from yatage.game import Game
import argparse


def cli() -> None:
    arg_parser = argparse.ArgumentParser(description='The YATAGE CLI which main purpose is to parse and run a YATAGE world file.')
    arg_parser.add_argument('world', help='Path to the YATAGE world file (*.yml) to load')

    args = arg_parser.parse_args()

    game = Game(args.world)
    game.run()
