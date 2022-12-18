from yatage.engine import Engine
import argparse


def run() -> None:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('world', help='Path to the YATAGE world file to load')

    args = arg_parser.parse_args()

    engine = Engine(args.world)
    engine.run()


if __name__ == '__main__':
    run()
