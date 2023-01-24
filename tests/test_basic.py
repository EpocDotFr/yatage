from typing import Optional, List
from yatage.game import Game


def run_basic_suite(
    world_filename: str,
    actions_filename: Optional[str] = None,
    additional_actions: List[str] = []
) -> None:
    for debug in (True, False):
        g = Game(world_filename, actions_filename, debug)

        if additional_actions:
            g.cmdqueue.extend(additional_actions)

        g.run()


def test_short() -> None:
    run_basic_suite('examples/short.yml', 'examples/short_actions.txt')


def test_synacor_challenge() -> None:
    run_basic_suite(
        'examples/synacor_challenge.yml',
        'examples/synacor_challenge_actions.txt',
        ['exit']
    )
