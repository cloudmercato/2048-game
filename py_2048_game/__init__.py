"""Package for 2048 Game logic."""
VERSION = (0, 1)
__version__ = '.'.join([str(i) for i in VERSION])
__email__ = 'anthony@cloud-mercato.com'
__author__ = 'Anthony Monthe'
__url__ = ''

from .core import Game
