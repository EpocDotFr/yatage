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
            item = self.current_room.get_item(subject)

            if item:
                self.text(item.definition.textual())
            else:
                self.text('You see no such item.')
        else:
            self.text(self.current_room.textual())

    def do_go(self, exit_: str) -> None:
        """You may 'go <exit>' to travel in that direction (such as 'go west'), or you may merely '<exit>' (such as 'west')."""
        self.text('I don\'t understand; try \'help\' for instructions.')

    def do_inv(self) -> None:
        """To see the contents of your inventory, merely 'inv'."""
        pass

    def do_take(self, item: str) -> None:
        """You may 'take <item>' (such as 'take large rock')."""
        pass

    def do_drop(self, item: str) -> None:
        """To drop something in your inventory, you may 'drop <item>'."""
        pass

    def do_use(self, item: str) -> None:
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
