import importlib
import numpy as np


class BaseSolver:
    def solve(self, game):
        raise NotImplementedError("Method is missing.")

    def solve_game(self, game):
        while not game.game_over():
            yield self.solve(game)


class RandomSolver(BaseSolver):
    def solve(self, game):
        avai_actions = game.available_actions()
        action = np.random.choice(avai_actions)
        reward = game.do_action(action)
        return (
            game.state,
            action,
            reward
        )


def get_solver(path):
    class_name = path.split('.')[-1]
    module_path = '.'.join([i for i in path.split('.')][:-1])
    solvers = importlib.import_module(module_path)
    solver = getattr(solvers, class_name)
    return solver
