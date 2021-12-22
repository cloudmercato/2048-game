import importlib
from py_2048_game.xp import xp as np
from py_2048_game import utils


class BaseSolver:
    def pre_solve(self, game):
        pass

    def post_solve(self, game):
        pass

    def solve(self, game):
        raise NotImplementedError("Method is missing.")

    def solve_game(self, game):
        while not game.game_over():
            self.pre_solve(game)
            output = self.solve(game)
            self.post_solve(game)
            yield output


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


class FirstActionSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.action = 0

    def pre_solve(self, game):
        if not game.is_action_available(self.action):
            self.action = 0 if self.action == 3 else (self.action + 1)

    def solve(self, game):
        reward = game.do_action(self.action)
        return (
            game.state,
            self.action,
            reward
        )


DEFAULT_SOLVER = RandomSolver


def get_solver(path=None):
    if path is None:
        return DEFAULT_SOLVER
    class_name = path.split('.')[-1]
    module_path = '.'.join([i for i in path.split('.')][:-1])
    solvers = importlib.import_module(module_path)
    solver = getattr(solvers, class_name)
    return solver
