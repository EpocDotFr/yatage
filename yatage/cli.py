from yatage.exceptions import WorldReadError
from yatage.game import Game
import argparse
# For The Loding Scene
import os
from yatage.ascii import loding
from asciimatics.effects import Cycle, Stars, BannerText, Print
from asciimatics.renderers import FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen


def cli() -> None:
    arg_parser = argparse.ArgumentParser(description='The YATAGE CLI which main purpose is to parse and run a YATAGE world file.')
    arg_parser.add_argument('world', help='Path to the YATAGE world file (*.yml) to load')
    arg_parser.add_argument('--actions', help='Path to the automatic actions file to perform')
    arg_parser.add_argument('--debug', action='store_true', help='Enable debug statements')

    args = arg_parser.parse_args()

    try:
        Screen.wrapper(loading)
        game = Game(args.world, args.actions, args.debug)
    except WorldReadError as e:
        print(f'Invalid world file "{args.world}": {e}')
    else:
        game.run()