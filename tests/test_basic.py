from yatage.game import Game


def test_basic():
    Game('examples/short.yml', 'examples/short_actions.txt').run()
