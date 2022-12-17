import cmd


class Loop(cmd.Cmd):
    prompt = '> '

    def postloop(self):
        print()

    def do_look(self, subject: str):
        """You may merely 'look' to examine the room, or you may 'look <subject>' (such as 'look chair') to examine something specific."""
        pass

    def do_go(self, exit_: str):
        """You may 'go <exit>' to travel in that direction (such as 'go west'), or you may merely '<exit>' (such as 'west')."""
        pass

    def do_inv(self):
        """To see the contents of your inventory, merely 'inv'."""
        pass

    def do_take(self, item: str):
        """You may 'take <item>' (such as 'take large rock')."""
        pass

    def do_drop(self, item: str):
        """To drop something in your inventory, you may 'drop <item>'."""
        pass

    def do_use(self, item: str):
        """You may activate or otherwise apply an item with 'use <item>'."""
        pass

    def default(self, line: str):
        pass # TODO go
