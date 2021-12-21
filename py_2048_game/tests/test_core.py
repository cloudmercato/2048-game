from unittest import TestCase
import numpy as np
from py_2048_game import core


class GameInitTest(TestCase):
    def test_init(self):
        game = core.Game()
        self.assertIsNotNone(game.state)
        self.assertEqual(game.score, 0)

    def test_init_withstate(self):
        state = np.zeros((4, 4), dtype=int)
        game = core.Game(state=state)
        self.assertTrue((game.state == state).any())


class GameTest(TestCase):
    def test_copy(self):
        game = core.Game()
        game2 = game.copy()
        self.assertTrue((game.state == game2.state).any())

    def test_add_random_tile(self):
        state = np.zeros((4, 4), dtype=int)
        game = core.Game(state=state)
        for i in range(3):
            game.add_random_tile()
            self.assertTrue(game.state.any())
            self.assertEqual(len(np.where(game.state > 0)[0]), i+1, game.state)

    def test_game_over_is_false(self):
        game = core.Game()
        self.assertFalse(game.game_over())

    def test_game_over_is_true(self):
        state = np.ones((4, 4), dtype=int)
        state[0::2,0::2] = 8
        state[1::2,1::2] = 32
        game = core.Game(state=state)
        self.assertTrue(game.game_over())


class GameDoActionTest(TestCase):
    def test_no_reward(self):
        state = np.zeros((4, 4), dtype=int)
        state[1][1] = 1
        game = core.Game(state=state)
        reward = game.do_action(0)
        self.assertEqual(reward, 0)
        self.assertEqual(game.score, 0)
        self.assertEqual(game.state[1][0], 1, game.state)
        self.assertEqual(len(np.where(game.state > 0)[0]), 2, game.state)

    def test_with_reward(self):
        state = np.zeros((4, 4), dtype=int)
        state[1] = 1
        game = core.Game(state=state)
        reward = game.do_action(0)
        self.assertEqual(reward, 8)
        self.assertEqual(game.score, 8)
        self.assertEqual(game.state[1][0], 2, game.state)
        self.assertEqual(game.state[1][1], 2, game.state)
        self.assertEqual(len(np.where(game.state > 0)[0]), 3, game.state)


class GameAvailableActionsTest(TestCase):
    def test_with_new(self):
        state = np.zeros((4, 4), dtype=int)
        state[1][1] = 1
        game = core.Game(state=state)
        self.assertEqual(game.available_actions(), [0, 1, 2, 3], game.state)

    def test_without_left(self):
        state = np.zeros((4, 4), dtype=int)
        state[1][0] = 1
        game = core.Game(state=state)
        self.assertEqual(game.available_actions(), [1, 2, 3], game.state)

    def test_without_up(self):
        state = np.zeros((4, 4), dtype=int)
        state[0][1] = 1
        game = core.Game(state=state)
        self.assertEqual(game.available_actions(), [0, 2, 3], game.state)

    def test_without_right(self):
        state = np.zeros((4, 4), dtype=int)
        state[1][3] = 1
        game = core.Game(state=state)
        self.assertEqual(game.available_actions(), [0, 1, 3], game.state)

    def test_without_down(self):
        state = np.zeros((4, 4), dtype=int)
        state[3][1] = 1
        game = core.Game(state=state)
        self.assertEqual(game.available_actions(), [0, 1, 2], game.state)

    def test_nothing(self):
        state = np.ones((4, 4), dtype=int)
        state[0::2,0::2] = 8
        state[1::2,1::2] = 32
        game = core.Game(state=state)
        self.assertFalse(game.available_actions(), game.state)
