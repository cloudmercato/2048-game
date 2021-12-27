import tensorflow as tf
from py_2048_game import core
from py_2048_game.xp import xp as np
from py_2048_game import utils


class Game(core.Game):
    def __init__(self, *args, **kwargs):
        self.keep_history = False

        self.score = tf.Variable(0)
        self.move_count = tf.Variable(0)

        self.state = tf.Variable(np.zeros((4, 4), dtype=float))
        self.add_random_tile()
        self.add_random_tile()

    def do_action(self, action):
        temp_state = np.rot90(self.state, action)
        reward = self._do_action_left(temp_state)
        self.state.assign(np.rot90(temp_state, -action))
        self.score.assign_add(reward)
        self.move_count.assign_add(reward)

        self.add_random_tile()
        self._record()

        return reward

    def reset(self):
        self.state.assign(np.zeros((4, 4)))
        self.add_random_tile()
        self.add_random_tile()
        self.move_count.assign(0)
        self.score.assign(0)
        self.history = {}
        self._record()

    def add_random_tile(self):
        x_pos, y_pos = np.where(self.state == 0)
        # Rerurn if no suitable tile exists.
        if len(x_pos) == 0:
            return
        empty_index = utils.random_choice(len(x_pos))
        value = utils.random_choice([2, 2], p=[0.9, 0.1])
        self.state[x_pos[empty_index], y_pos[empty_index]].assign(value)
