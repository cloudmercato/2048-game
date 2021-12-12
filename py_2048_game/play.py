import sys
import tty
import termios
from py_2048_game.core import Game

KEYS = {
    '\x1b[D': 0,
    '\x1b[B': 1,
    '\x1b[C': 2,
    '\x1b[A': 3,
}


def wait_action():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    while 1:
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(3)
            print(key)
        except IOError:
            pass
        if key in 'qc':
            return
        if key in KEYS:
            break
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    action = KEYS[key]
    return action

game = Game()
while 1:
    game.print_state()
    action = wait_action()
    print(action)
    game.do_action(int(action))
