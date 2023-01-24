from yatage.__version__ import __version__ as yatage_version
from yatage.inventory import Inventory
from yatage.commands import Commands
from yatage.world import World
from yatage.room import Room
from typing import Optional


class Game(Commands):
    world_filename: str
    actions_filename: Optional[str]
    debug: bool

    world: World
    current_room: Room
    inventory: Inventory
    intro: str

    def __init__(self, world_filename: str, actions_filename: Optional[str] = None, debug: bool = False) -> None:
        self.world_filename = world_filename
        self.actions_filename = actions_filename
        self.debug = debug

        with open(self.world_filename, 'r') as fp:
            self.world = World.load(self, fp)

        self.current_room = self.world.start
        self.inventory = Inventory(self)

        super().__init__()

        self.intro = self.create_intro()

        self.load_actions()

    def create_intro(self, include_current_room: bool = True) -> str:
        header = '#' * len(self.world.name)

        text = [
            header,
            self.world.name,
            header,
        ]

        if self.debug:
            text.extend((
                '',
                f'YATAGE version: {yatage_version}',
                f'World file version: {self.world.version}',
                f'Rooms: {len(self.world.rooms)}',
                f'Items: {len(self.world.items)}',
            ))

        if self.world.author:
            text.extend((
                '',
                f'By {self.world.author}',
            ))

        if self.world.description:
            text.extend((
                '',
                self.world.description,
            ))

        if include_current_room:
            text.extend((
                '',
                self.current_room.look(),
            ))

        return '\n'.join(text)

    def load_actions(self) -> None:
        if not self.actions_filename:
            return

        with open(self.actions_filename, 'r') as fp:
            for line in fp:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                line = line.split('#', maxsplit=1)[0].strip()

                self.cmdqueue.append(line)


__all__ = [
    'Game',
]
