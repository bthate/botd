# BOTD - python3 IRC channel daemon.
#
# terminal code.

import atexit
import sys
import termios

resume = {}

def reset():
    if "old" in resume:
        termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])

def save():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = setup(sys.stdin.fileno())
        atexit.register(reset)
    except termios.error:
        pass    

def setup(fd):
    return termios.tcgetattr(fd)
