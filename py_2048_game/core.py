"""Game class to represent 2048 game state."""

import logging
import importlib
from py_2048_game.xp import xp as np
from py_2048_game import utils

ACTION_LEFT = 0
ACTION_UP = 1
ACTION_RIGHT = 2
ACTION_DOWN = 3

logger = logging.getLogger('py2048_game')


class Game:
    """Represents a 2048 Game state and implements the actions.

    Implements the 2048 Game logic, as specified by this source file:
    https://github.com/gabrielecirulli/2048/blob/master/js/game_manager.js

    Game states are represented as shape (4, 4) numpy arrays whos entries are 0
    for empty fields and ln2(value) for any tiles.
    """

    def __init__(self, state=None, initial_score=0, seed=None, keep_history=True):
        """Init the Game object.

        Args:
            state: Shape (4, 4) numpy array to initialize the state with. If None,
                    the state will be initialized with with two random tiles (as done
                    in the original game).
            initial_score: Score to initialize the Game with.
        """

        self.score = initial_score
        self.history = {}
        self.keep_history = keep_history

        if state is None:
            self.state = np.zeros((4, 4), dtype=int)
            self.add_random_tile()
            self.add_random_tile()
        else:
            self.state = state
        self._seed = seed
        if seed is not None:
            np.random.seed(seed)
        self.move_count = 0
        self._record()

    def _record(self):
        if not self.keep_history:
            return
        self.history[self.move_count] = ((self.state.copy(), self.move_count, self.score))

    def copy(self, seed=None):
        """Return a copy of self."""
        seed = seed or self._seed
        return Game(
            np.copy(self.state),
            self.score,
            seed=seed,
        )

    def reset(self):
        self.state[:] = 0
        self.add_random_tile()
        self.add_random_tile()
        self.move_count = 0
        self.score = 0
        self.history = {}
        self._record()

    def game_over(self):
        """Whether the game is over."""
        for action in range(4):
            if self.is_action_available(action):
                return False
        return True

    def available_actions(self):
        """Computes the set of actions that are available."""
        return [
            action for action in range(4)
            if self.is_action_available(action)
        ]

    def is_action_available(self, action):
        """Determines whether action is available.
        That is, executing it would change the state.
        """

        temp_state = np.rot90(self.state, action)
        return self._is_action_available_left(temp_state)

    def _is_action_available_left(self, state):
        """Determines whether action 'Left' is available."""

        # True if any field is 0 (empty) on the left of a tile or two tiles can
        # be merged.
        for row in range(4):
            has_empty = False
            for col in range(4):
                has_empty |= state[row, col] == 0
                if state[row, col] != 0 and has_empty:
                    return True
                if (state[row, col] != 0 and col > 0 and
                        state[row, col] == state[row, col - 1]):
                    return True

        return False

    def do_action(self, action):
        """Execute action, add a new tile, update the score & return the reward."""

        temp_state = np.rot90(self.state, action)
        reward = self._do_action_left(temp_state)
        self.state = np.rot90(temp_state, -action)
        self.score += reward
        self.move_count += 1

        self.add_random_tile()
        self._record()

        return reward

    def _do_action_left(self, state):
        """Exectures action 'Left'."""

        reward = 0

        for row in range(4):
            # Always the rightmost tile in the current row that was already moved
            merge_candidate = -1
            merged = np.zeros((4,), dtype=bool)

            for col in range(4):
                if state[row, col] == 0:
                    continue

                if (merge_candidate != -1 and
                        not merged[merge_candidate] and
                        state[row, merge_candidate] == state[row, col]):
                    # Merge tile with merge_candidate
                    state[row, col] = 0
                    merged[merge_candidate] = True
                    state[row, merge_candidate] += 1
                    reward += 2 ** state[row, merge_candidate]

                else:
                    # Move tile to the left
                    merge_candidate += 1
                    if col != merge_candidate:
                        state[row, merge_candidate] = state[row, col]
                        state[row, col] = 0

        return reward

    def add_random_tile(self):
        """Adds a random tile to the grid. Assumes that it has empty fields."""
        x_pos, y_pos = np.where(self.state == 0)

        # Rerurn if no suitable tile exists.
        if len(x_pos) == 0:
            return

        empty_index = utils.random_choice(len(x_pos))
        value = utils.random_choice([2, 2], p=[0.9, 0.1])

        self.state[x_pos[empty_index], y_pos[empty_index]] = value

    def undo(self, step=1):
        if not self.keep_history:
            return
        index = self.move_count - step
        if index not in self.history:
            return
        state, move_count, score = self.history[index]
        self.score = score
        self.move_count = move_count
        self.state = state.copy()

    def redo(self, step=1):
        if not self.keep_history:
            return
        index = self.move_count + step
        if index not in self.history:
            return
        state, move_count, score = self.history[index]
        self.score = score
        self.move_count = move_count
        self.state = state.copy()


DEFAULT_GAME = Game


def get_game_class(path=None):
    if path is None:
        return DEFAULT_GAME
    class_name = path.split('.')[-1]
    module_path = '.'.join([i for i in path.split('.')][:-1])
    module = importlib.import_module(module_path)
    klass = getattr(module, class_name)
    return klass
