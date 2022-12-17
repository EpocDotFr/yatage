import cmd


class Loop(cmd.Cmd):
    prompt = '> '

    def __init__(self, game):
        self.game = game

        super().__init__()

    def postloop(self):
        print()

    def do_look(self, subject):
        """You may merely 'look' to examine the room, or you may 'look <subject>' (such as 'look chair') to examine something specific."""
        pass

    def do_go(self, exit_):
        """You may 'go <exit>' to travel in that direction (such as 'go west'), or you may merely '<exit>' (such as 'west')."""
        pass

    def do_inv(self):
        """To see the contents of your inventory, merely 'inv'."""
        pass

    def do_take(self, item):
        """You may 'take <item>' (such as 'take large rock')."""
        pass

    def do_drop(self, item):
        """To drop something in your inventory, you may 'drop <item>'."""
        pass

    def do_use(self, item):
        """You may activate or otherwise apply an item with 'use <item>'."""
        pass

    def default(self, line):
        pass # TODO go


class Game:
    def __init__(self):
        self.loop = Loop(self)
        # self.loop.intro = '' # TODO

    def load(self, filename):
        pass

    def run(self):
        self.loop.cmdloop()
