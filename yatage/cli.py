import argparse
import yatage


def cli() -> None:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('world', help='Path to the YATAGE world file to load')

    args = arg_parser.parse_args()

    game = yatage.Game(args.world)
    game.run()
