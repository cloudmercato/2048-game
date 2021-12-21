import time
import curses
from curses.textpad import rectangle
import argparse

from py_2048_game.core import Game

MOVES = {
    curses.KEY_LEFT: 0,
    curses.KEY_UP: 1,
    curses.KEY_RIGHT: 2,
    curses.KEY_DOWN: 3,
}
ACTIONS = {
    113: 'quit',
    114: 'redo',
    115: 'solve',
    117: 'undo',
}

def curses_main(stdscr, seed=None, solver=None, keep_history=True):
    stdscr.clear()

    if solver is not None:
        stdscr.addstr(1, 13, '(s)olve')
    if keep_history:
        stdscr.addstr(2, 13, '(u)ndo')
        stdscr.addstr(3, 13, '(r)edo')
    stdscr.addstr(5, 13, '(q)uit')

    game = Game(seed=seed, keep_history=keep_history)
    rectangle(stdscr, 0, 0, 2+3, 2+8)

    while 1:
        for i, (a, b, c, d) in enumerate(game.state):
            stdscr.addstr(i+1, 2, '%s %s %s %s' % (a, b, c, d))
        stdscr.addstr(6, 0, 'Round: %s' % game.move_count)
        stdscr.addstr(7, 0, 'Score: %s' % game.score)

        reward = 0
        while 1:
            key = stdscr.getch()
            if key in MOVES or key in ACTIONS:
                break

        if key in MOVES:
            action = MOVES[key]
            reward = game.do_action(action)
        elif key == 113:
            raise KeyboardInterrupt()
        elif key == 114 and keep_history:
            game.redo()
        elif key == 117 and keep_history:
            game.undo()
        elif key == 115:
            _, _, reward = solver.solve(game)

        if reward:
            stdscr.addstr(8, 6, '+%d' % reward)
        else:
            stdscr.addstr(8, 6, ' '*10)

        if game.game_over():
            stdscr.addstr(9, 0, 'GAME OVER')
            stdscr.getch()
            time.sleep(3)
            break

        stdscr.refresh()

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--seed', type=int)

def main(**kwargs):
    try:
        curses.wrapper(
            curses_main,
            seed=kwargs.get('seed'),
            solver=kwargs.get('solver'),
            keep_history=kwargs.get('keep_history'),
        )
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    args = parser.parse_args()
    main(
        seed=args.seed,
    )
