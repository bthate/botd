# BOTLIB - the bot library !
#
#

import atexit, argparse, grp, logging, os, pwd, readline, sys, termios, time, _thread

from .obj import Cfg
from .prs import Parsed
from .fil import cdir

cmds = []
logfile = ""
resume = {}
HISTFILE = ""

def bexec(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")

def close_history():
    global HISTFILE
    if bot.obj.workdir:
        if not HISTFILE:
            HISTFILE = os.path.join(bot.obj.workdir, "history")
        if not os.path.isfile(HISTFILE):
            cdir(HISTFILE)
            touch(HISTFILE)
        readline.write_history_file(HISTFILE)

def complete(text, state):
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def daemon():
    pid = os.fork()
    if pid != 0:
        termreset()
        os._exit(0)
    os.setsid()
    pid = os.fork()
    if pid != 0:
        termreset()
        os._exit(0)
    os.umask(0)
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def drop():
    ruid = pwd.getpwnam("botd")[2]
    os.setuid(ruid)
    os.umask(0o007)

def enable_history():
    assert bot.obj.workdir
    HISTFILE = os.path.abspath(os.path.join(bot.obj.workdir, "history"))
    if not os.path.exists(HISTFILE):
        cdir(HISTFILE)
        touch(HISTFILE)
    else:
        readline.read_history_file(HISTFILE)
    atexit.register(close_history)

def execute(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")
    finally:
        termreset()

def get_completer():
    return readline.get_completer()

def level(loglevel, nostream=False):
    if not loglevel:
        loglevel = "error"
    if logfile and not os.path.exists(logfile):
        cdir(logfile)
        touch(logfile)
    datefmt = '%H:%M:%S'
    format_time = "%(asctime)-8s %(message)-70s"
    format_plain = "%(message)-0s"
    loglevel = loglevel.upper()
    logger = logging.getLogger("")
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    try:
        logger.setLevel(loglevel)
    except ValueError:
        pass
    formatter = logging.Formatter(format_plain, datefmt)
    if nostream:
        dhandler = DumpHandler()
        dhandler.propagate = False
        dhandler.setLevel(loglevel)
        logger.addHandler(dhandler)
    else:
        handler = logging.StreamHandler()
        handler.propagate = False
        handler.setFormatter(formatter)
        try:
            handler.setLevel(loglevel)
            logger.addHandler(handler)
        except ValueError:
            loglevel = "ERROR"
    if logfile:
        formatter2 = logging.Formatter(format_time, datefmt)
        filehandler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight')
        filehandler.propagate = False
        filehandler.setFormatter(formatter2)
        try:
            filehandler.setLevel(loglevel)
        except ValueError:
            pass
        logger.addHandler(filehandler)
    return logger

def parse_cli():
    setwd()
    if len(sys.argv) <= 1:
        return Cfg()
    p = Parsed()
    p.parse(" ".join(sys.argv[1:]))
    cfg = Cfg()
    cfg.name = "bot"
    cfg.update(p.sets)
    return cfg

def root():
    if os.geteuid() != 0:
        return False
    return True

def setcompleter(commands):
    global cmds
    cmds = commands
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))
        
def setup(fd):
    return termios.tcgetattr(fd)

def setwd():
    import bot.obj
    if root():
        bot.obj.workdir = "/var/lib/botd"
    else:
        bot.obj.workdir = os.path.expanduser("~/.bot")

def termreset():
    if "old" in resume:
        termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])

def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = setup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass    

def writepid():
    assert bot.obj.workdir
    path = os.path.join(bot.obj.workdir, "pid")
    if not os.path.exists(path):
        cdir(path)
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()
