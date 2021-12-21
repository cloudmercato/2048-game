from py_2048_game import xp


def random_choice(a, size=None, replace=True, p=None):
    choice = xp.xp.random.choice(a, size=size or 1, p=p)
    if size is None:
        choice = choice[0]
    return choice


def get_versions():
    string = 'numpy: %s' % xp.np.__version__
    if xp.cp is not None:
        string += ' cupy: %s' % xp.cp.__version__
    return string


def print_state(game):
    """Prints the game state."""
    def tile_string(value):
        """Concert value to string."""
        if value > 0:
            return '% 5d' % (2 ** value,)
        return "         "

    print("-" * 25)
    for row in range(4):
        print("|" + "|".join([
            tile_string(v) for v in game._state[row, :]
        ]) + "|")
        print("-" * 25)
