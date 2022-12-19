from yatage.game import Game
import argparse


def cli() -> None:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('world', help='Path to the YATAGE world file to load')

    args = arg_parser.parse_args()

    game = Game(args.world)
    game.run()
