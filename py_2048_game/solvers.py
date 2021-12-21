import importlib
from py_2048_game.xp import xp as np
from py_2048_game import utils


class BaseSolver:
    def solve(self, game):
        raise NotImplementedError("Method is missing.")

    def solve_game(self, game):
        while not game.game_over():
            yield self.solve(game)


class RandomSolver(BaseSolver):
    def solve(self, game):
        avai_actions = game.available_actions()
        action = utils.random_choice(avai_actions)
        reward = game.do_action(action)
        return (
            game.state,
            action,
            reward
        )


def get_solver(path=None):
    if path is None:
        return RandomSolver
    class_name = path.split('.')[-1]
    module_path = '.'.join([i for i in path.split('.')][:-1])
    solvers = importlib.import_module(module_path)
    solver = getattr(solvers, class_name)
    return solver
