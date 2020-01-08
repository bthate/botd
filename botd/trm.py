# BOTD - python3 IRC channel daemon.
#
# terminal code.

import atexit
import sys
import termios

resume = {}

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

def setup(fd):
    return termios.tcgetattr(fd)
