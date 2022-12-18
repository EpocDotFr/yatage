from yatage.engine import Engine
from yatage.world import World
from yatage.loop import Loop


class Game:
    def __init__(self, world_filename: str) -> None:
        self.loop = Loop()
        self.engine = Engine()
        self.world = World.load(world_filename)

        self.loop.intro = self.world.description

    def run(self) -> None:
        try:
            self.loop.cmdloop()
        except KeyboardInterrupt:
            pass
