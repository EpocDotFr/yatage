from yatage.inventory import Inventory
from yatage.utils import get_item
from yatage.world import World
from yatage.room import Room
from yatage.loop import Loop
from typing import Optional


class Game(Loop):
    world_filename: str
    world: World
    current_room: Room
    inventory: Inventory

    def __init__(self, world_filename: str) -> None:
        super().__init__()

        self.world_filename = world_filename
        self.world = World.load(self)
        self.current_room = self.world.start
        self.inventory = Inventory(self)

        self.intro = self.create_intro()

    def do_look(self, subject: str) -> Optional[bool]:
        """You may merely 'look' to examine the room, or you may 'look <subject>' (such as 'look chair') to examine something specific."""
        if subject:
            item = get_item(self.current_room.items, subject) or get_item(self.inventory, subject)

            if item:
                self.line(item.do_look())
            else:
                self.line('You see no such item.')
        else:
            self.line(self.current_room.do_look())

    def do_go(self, exit_: str) -> Optional[bool]:
        """You may 'go <exit>' to travel in that direction (such as 'go west'), or you may merely '<exit>' (such as 'west')."""
        if exit_ in self.current_room.exits:
            self.current_room = self.current_room.exits.get(exit_)

            self.line(self.current_room.do_look())
        else:
            self.line('I don\'t understand; try \'help\' for instructions.')

    def do_inv(self, _: str) -> Optional[bool]:
        """To see the contents of your inventory, merely 'inv'."""
        self.line(self.inventory.do_look())

    def do_take(self, item_identifier: str) -> Optional[bool]:
        """You may 'take <item>' (such as 'take large rock')."""
        if self.inventory.take(item_identifier):
            self.line('Taken.')
        else:
            self.line('You see no such item.')

    def do_drop(self, item_identifier: str) -> Optional[bool]:
        """To drop something in your inventory, you may 'drop <item>'."""
        if self.inventory.drop(item_identifier):
            self.line('Dropped.')
        else:
            self.line('You can\'t find that in your pack.')

    def do_use(self, item_identifier: str) -> Optional[bool]:
        """You may activate or otherwise apply an item with 'use <item>'."""
        item = get_item(self.inventory, item_identifier)

        if item:
            use_result = item.do_use()

            if isinstance(use_result, str):
                self.line(use_result)
        else:
            self.line('You can\'t find that in your pack.')

    def default(self, line: str) -> Optional[bool]:
        return self.do_go(line)

    def create_intro(self) -> str:
        text = [
            self.world.name,
            '=' * len(self.world.name),
        ]

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

        text.extend((
            '',
            self.current_room.do_look(),
        ))

        return '\n'.join(text)


__all__ = [
    'Game',
]
