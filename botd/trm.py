# BOTD - IRC channel daemon.
#
# terminal code.

""" terminal handling code. """


import atexit
import sys
import termios

resume = {}

def termreset():
    """
        termreset function.
        
        reset the terminal to it's saved state.
        
    """
    if "old" in resume:
        termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])

def termsave():
    """
        termsave function.
        
        save the current terminal info

    """
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = setup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass    

def setup(fd):
    """
        setup function.
        
        return terminal attributes.
        
    """
    return termios.tcgetattr(fd)
