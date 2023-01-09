from yatage.room import GameOverExit, TextExit, ItemConditionedExit, Room
from yatage.inventory import Inventory
from typing import List, Optional
from yatage.world import World
from yatage.loop import Loop
import yatage.utils


class Commands(Loop):
    debug: bool
    current_room: Room
    inventory: Inventory
    world: World

    commands: List[str] = [
        'look',
        'go',
        'inv',
        'take',
        'drop',
        'use',
    ]

    def __init__(self) -> None:
        super().__init__()

        if self.debug:
            self.commands.extend([
                'spawn',
                'tp',
            ])

        self.register_commands()

    def register_commands(self) -> None:
        for command in self.commands:
            setattr(self, f'do_{command}', getattr(self, command))

    def look(self, subject: str) -> Optional[bool]:
        """You may merely 'look' to examine the room, or you may 'look <subject>' (such as 'look chair') to examine something specific."""
        if subject:
            item = yatage.utils.get_item(self.current_room.items, subject) or yatage.utils.get_item(self.inventory, subject)

            if item:
                self.line(item.do_look())
            else:
                self.line('You see no such item.')
        else:
            self.line(self.current_room.do_look())

        return

    def go(self, exit_: str) -> Optional[bool]:
        """You may 'go <exit>' to travel in that direction (such as 'go west'), or you may merely '<exit>' (such as 'west')."""
        if exit_ in self.current_room.exits:
            exit_data = self.current_room.exits.get(exit_)

            if isinstance(exit_data, ItemConditionedExit):
                exit_data = exit_data.do_exit()

            if isinstance(exit_data, Room):
                self.current_room = exit_data

                self.line(self.current_room.do_look())
            elif isinstance(exit_data, GameOverExit):
                self.line(exit_data.text)

                return True
            elif isinstance(exit_data, TextExit):
                self.line(exit_data.text)

                if exit_data.exit:
                    self.current_room = exit_data.exit

                    self.line('')
                    self.line(self.current_room.do_look())
        else:
            self.line('I don\'t understand; try \'help\' for instructions.')

        return

    def inv(self, _: str) -> Optional[bool]:
        """To see the contents of your inventory, merely 'inv'."""
        self.line(self.inventory.do_look())

        return

    def take(self, item_identifier: str) -> Optional[bool]:
        """You may 'take <item>' (such as 'take large rock')."""
        if self.inventory.take(item_identifier):
            self.line('Taken.')
        else:
            self.line('You see no such item.')

        return

    def drop(self, item_identifier: str) -> Optional[bool]:
        """To drop something in your inventory, you may 'drop <item>'."""
        if self.inventory.drop(item_identifier):
            self.line('Dropped.')
        else:
            self.line('You can\'t find that in your pack.')

        return

    def use(self, item_identifier: str) -> Optional[bool]:
        """You may activate or otherwise apply an item with 'use <item>'."""
        if not self.inventory.use(item_identifier):
            self.line('You can\'t find that in your pack.')

        return

    def spawn(self, item_identifier: str) -> Optional[bool]:
        """Debug: Spawn an item into inventory with 'spawn <item>'."""
        if self.inventory.spawn(item_identifier):
            self.line('Spawned.')
        else:
            self.line('Unknown item.')

        return

    def tp(self, room_identifier: str) -> Optional[bool]:
        """Debug: Teleport to the given room with 'tp <room>'."""
        if room_identifier not in self.world.rooms:
            self.line('Unknown room.')

            return

        self.current_room = self.world.rooms.get(room_identifier)

        self.line(self.current_room.do_look())

        return

    def default(self, line: str) -> Optional[bool]:
        return self.go(line)
