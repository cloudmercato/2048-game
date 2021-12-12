from setuptools import setup, find_packages
import py_2048_game


def read_file(name):
    with open(name) as fd:
        return fd.read()

setup(
    name="2048-game",
    version=py_2048_game.__version__,
    author=py_2048_game.__author__,
    author_email=py_2048_game.__email__,
    description=py_2048_game.__doc__,
    url=py_2048_game.__url__,
    # keywords=py_2048_game.__keywords__,
    # license=py_2048_game.__license__,
    py_modules=['py_2048_game'],
    packages=find_packages(),
    install_requires=read_file('requirements.txt').splitlines(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.6',
    ],
    long_description=read_file('README.rst'),
    # entry_points={'console_scripts': [
    #     'cb-client = py_2048_game.console:main',
    # ]},
)
