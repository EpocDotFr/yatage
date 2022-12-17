from yatage.engine import Engine
from yatage.world import World
from yatage.loop import Loop


class Game:
    def __init__(self, filename: str):
        self.loop = Loop()
        self.engine = Engine()
        self.world = World.load(filename)

        self.loop.intro = self.world.description

    def run(self):
        self.loop.cmdloop()
