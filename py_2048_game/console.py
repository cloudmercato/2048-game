import os
import argparse
import logging

from py_2048_game import play_curses
from py_2048_game import solvers
from py_2048_game import Game
from py_2048_game import utils

logger = logging.getLogger('py2048_game')

parser = argparse.ArgumentParser()
parser.add_argument('action', default='solver', choices=('curses', 'solver'), nargs='?')
parser.add_argument('--solver', '-s', default='py_2048_game.solvers.RandomSolver')
parser.add_argument('--verbose', '-v', default=3, type=int)
parser.add_argument('--version', '-V', default=False, action="store_true")


def main():
    args = parser.parse_args()

    log_verbose = 50 - (args.verbose*10)
    log_handler = logging.StreamHandler()
    log_handler.setLevel(log_verbose)
    logger.addHandler(log_handler)
    logger.setLevel(log_verbose)

    if args.version:
        print(utils.get_versions())
        exit(0)
    elif args.action == 'curses':
        solver = solvers.get_solver(args.solver)()
        play_curses.main(
            solver=solver,
        )
    elif args.action == 'solver':
        solver = solvers.get_solver(args.solver)()
        game = Game()
        for _, action, reward in solver.solve_game(game):
            logger.debug('Move: %s Score: %s', game.move_count, game.score)
        logger.info('Score: %s', game.score)

if __name__ == "__main__":
    main()
