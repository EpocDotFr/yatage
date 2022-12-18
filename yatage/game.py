from yatage.world import World, Room, Item
from typing import Optional, List
import cmd


class Game(cmd.Cmd):
    prompt: str = '\nWhat do you do?\n> '
    current_room: Optional[Room] = None
    inventory: List[Item]

    def __init__(self, world_filename: str) -> None:
        super().__init__()

        self.world = World.load(world_filename)
        self.current_room = self.world.start
        self.intro = self.world.description + '\n\n' + self.world.start.textual()
        self.inventory = []

    def do_look(self, subject: str) -> None:
        """You may merely 'look' to examine the room, or you may 'look <subject>' (such as 'look chair') to examine something specific."""
        if subject:
            item_object = self.current_room.get_item(subject)

            if item_object:
                self.text(item_object.definition.textual())
            else:
                self.text('You see no such item.')
        else:
            self.text(self.current_room.textual())

    def do_go(self, exit_: str) -> None:
        """You may 'go <exit>' to travel in that direction (such as 'go west'), or you may merely '<exit>' (such as 'west')."""
        self.text('I don\'t understand; try \'help\' for instructions.')

    def do_inv(self, _: str) -> None:
        """To see the contents of your inventory, merely 'inv'."""
        text = [
            'Your inventory:',
        ]

        for item in self.inventory:
            text.append(f'- {item.definition.identifier}')

        self.text('\n'.join(text))

    def do_take(self, item_identifier: str) -> None:
        """You may 'take <item>' (such as 'take large rock')."""
        item_object = self.current_room.get_item(item_identifier)

        if item_object:
            self.inventory.append(
                self.current_room.items.pop(
                    self.current_room.items.index(item_object)
                )
            )

            self.text('Taken.')
        else:
            self.text('You see no such item.')

    def do_drop(self, item_identifier: str) -> None:
        """To drop something in your inventory, you may 'drop <item>'."""
        item_object = next(
            (item for item in self.inventory if item.definition.identifier == item_identifier),
            None
        )

        if item_object:
            self.current_room.items.append(
                self.inventory.pop(
                    self.inventory.index(item_object)
                )
            )

            self.text('Dropped.')
        else:
            self.text('You can\'t find that in your pack.')

    def do_use(self, item_identifier: str) -> None:
        """You may activate or otherwise apply an item with 'use <item>'."""
        pass

    def default(self, line: str) -> None:
        self.do_go(line)

    def postloop(self) -> None:
        self.text('', '')

    def do_EOF(self, line: str) -> bool:
        return True

    def text(self, text: str, start: str = '\n\n', end: str = '\n') -> None:
        self.stdout.write(f'{start}{text}{end}')

    def run(self) -> None:
        try:
            self.cmdloop()
        except KeyboardInterrupt:
            pass
