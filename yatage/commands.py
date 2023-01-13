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
                'destroy',
                'tp',
            ])

        self.register_commands()

    def register_commands(self) -> None:
        for command in self.commands:
            setattr(self, f'do_{command}', getattr(self, command))

    def look(self, item_identifier: str) -> Optional[bool]:
        """look
            Examine the current room.
        
        look <item>
            Examine item <item>. May be either an item in the current room or in the inventory."""
        if item_identifier:
            item = yatage.utils.get_item(self.current_room.items, item_identifier) or yatage.utils.get_item(self.inventory, item_identifier)

            if item:
                self.line(item.do_look())
            else:
                self.line('You see no such item.')
        else:
            self.line(self.current_room.do_look())

        return

    def go(self, exit_: str) -> Optional[bool]:
        """go <exit> or merely <exit>
        
        Travel to the direction <exit>."""
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
        """List items currently in inventory."""
        self.line(self.inventory.do_look())

        return

    def take(self, item_identifier: str) -> Optional[bool]:
        """take <item>
        
        Take item <item> from the current room and put it into the inventory."""
        if self.inventory.take(item_identifier):
            self.line('Taken.')
        else:
            self.line('You see no such item.')

        return

    def drop(self, item_identifier: str) -> Optional[bool]:
        """drop <item>
        
        Remove the item <item> from the inventory and drop it into the current room."""
        if self.inventory.drop(item_identifier):
            self.line('Dropped.')
        else:
            self.line('You can\'t find that in your pack.')

        return

    def use(self, item_identifier: str) -> Optional[bool]:
        """use <item>
        
        Activate or apply item <item>. Item must be present in inventory."""
        if not self.inventory.use(item_identifier):
            self.line('You can\'t find that in your pack.')

        return

    def spawn(self, item_identifier: str) -> Optional[bool]:
        """spawn <item>
        
        Spawn a new item identified by <item> into the player’s inventory."""
        if self.inventory.spawn(item_identifier):
            self.line('Spawned.')
        else:
            self.line('Unknown item.')

        return

    def destroy(self, item_identifier: str) -> Optional[bool]:
        """destroy <item>
        
        Destroy item identified by <item> in player’s inventory."""
        if self.inventory.destroy(item_identifier):
            self.line('Destroyed.')
        else:
            self.line('Unknown item.')

        return

    def tp(self, room_identifier: str) -> Optional[bool]:
        """tp <room>
        
        Teleport the player to the room identified by <room>."""
        if room_identifier not in self.world.rooms:
            self.line('Unknown room.')

            return

        self.current_room = self.world.rooms.get(room_identifier)

        self.line(self.current_room.do_look())

        return

    def default(self, line: str) -> Optional[bool]:
        return self.go(line)
