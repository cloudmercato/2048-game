import tensorflow as tf
from py_2048_game import core
from py_2048_game.xp import xp as np


class Game(core.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = tf.Variable(self.score)
        self.move_count = tf.Variable(self.move_count)
        self.state = tf.Variable(self.state)

    def do_action(self, action):
        temp_state = np.rot90(self.state, action)
        reward = self._do_action_left(temp_state)
        self.state = np.rot90(temp_state, -action)
        self.score.assign_add(reward)
        self.move_count.assign_add(reward)

        self.add_random_tile()
        self._record()

        return reward
