from yatage.world import World
from yatage.loop import Loop


class Engine:
    def __init__(self, world_filename: str) -> None:
        self.loop = Loop()
        self.world = World.load(world_filename)

        self.loop.intro = self.world.description + self.world.start.textual()

    def run(self) -> None:
        try:
            self.loop.cmdloop()
        except KeyboardInterrupt:
            pass
