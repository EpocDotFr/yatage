import cmd


class Loop(cmd.Cmd):
    prompt: str = '\nWhat do you do?\n> '

    def do_look(self, subject: str) -> None:
        """You may merely 'look' to examine the room, or you may 'look <subject>' (such as 'look chair') to examine something specific."""
        pass

    def do_go(self, exit_: str) -> None:
        """You may 'go <exit>' to travel in that direction (such as 'go west'), or you may merely '<exit>' (such as 'west')."""
        self.line('I don\'t understand; try \'help\' for instructions.')

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
        self.line()

    def do_EOF(self, line: str) -> bool:
        return True

    def line(self, text: str = '') -> None:
        self.stdout.write(f'{text}\n')
