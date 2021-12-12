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
