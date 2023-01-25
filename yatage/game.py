from yatage.room import GameOverExit, TextExit, ItemConditionedExit, Room
from yatage.__version__ import __version__ as yatage_version
from typing import Tuple, List, Optional
from yatage.inventory import Inventory
from yatage.world import World
from yatage.room import Room
from cmd import Cmd
import subprocess
import platform


class Game(Cmd):
    # Python's cmd.Cmd-related attributes #####################################

    prompt: str = '\nWhat do you do?\n===============\n> '
    doc_header: str = 'Available actions (type help <action>):'
    ruler: str = '^'
    hidden_commands: Tuple[str, ...] = ('do_EOF',)

    # YATAGE game attributes ##################################################

    world_filename: str
    actions_filename: Optional[str]
    debug: bool
    world: World
    current_room: Room
    inventory: Inventory
    intro: str

    # YATAGE commands attributes ##############################################

    commands: List[str] = []

    regular_commands: List[str] = [
        'look',
        'intro',
        'exit',
        'go',
        'inv',
        'take',
        'drop',
        'use',
    ]

    debug_commands: List[str] = [
        'spawn',
        'destroy',
        'tp',
    ]

    all_commands: List[str] = []

    def __init__(self, world_filename: str, actions_filename: Optional[str] = None, debug: bool = False) -> None:
        super().__init__()

        self.world_filename = world_filename
        self.actions_filename = actions_filename
        self.debug = debug

        with open(self.world_filename, 'r') as fp:
            self.world = World.load(self, fp)

        self.current_room = self.world.start
        self.inventory = Inventory(self)
        self.intro = self.create_intro()
        self.all_commands = self.regular_commands + self.debug_commands
        self.commands = self.all_commands if self.debug else self.regular_commands

        self.register_commands()

        self.load_actions()

    # Python's cmd.Cmd-related methods ########################################

    def preloop(self) -> None:
        self.clear_screen()

    def postloop(self) -> None:
        self.line('')

    def precmd(self, line) -> str:
        self.clear_screen()

        return line

    def do_EOF(self, _: str) -> Optional[bool]:
        return True

    def get_names(self) -> List:
        return [m for m in dir(self) if m not in self.hidden_commands]

    def line(self, text: str, end: str = '\n') -> None:
        self.stdout.write(f'{text}{end}')

    def print_help(self, lines: Tuple[str, ...]) -> None:
        self.line('\n'.join(lines))

    def clear_screen(self) -> None:
        if platform.system() == 'Windows' and platform.release() not in ('10', '11', 'post11'):
            subprocess.run('cls')
        else:
            self.line("\033[H\033[2J", '')

    def run(self) -> None:
        try:
            self.cmdloop()
        except KeyboardInterrupt:
            pass

    # YATAGE game methods #####################################################

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

    # YATAGE commands methods #################################################

    def register_commands(self) -> None:
        for command in self.commands:
            setattr(self, f'do_{command}', getattr(self, f'_{command}'))
            setattr(self, f'help_{command}', getattr(self, f'_{command}_help'))

    def _look(self, item_identifier: str) -> Optional[bool]:
        if item_identifier:
            item = self.current_room.get_item(item_identifier) or self.inventory.get(item_identifier)

            if item:
                self.line(item.look())
            else:
                self.line('You see no such item.')
        else:
            self.line(self.current_room.look())

        return

    def _look_help(self) -> None:
        self.print_help((
            'look',
            '    Examine the current room.',
            '',
            'look <item>',
            '    Examine item <item>. May be either an item in the current room or in the inventory.',
        ))

    def _intro(self, _: str) -> Optional[bool]:
        self.line(self.create_intro(False))

        return

    def _intro_help(self) -> None:
        self.print_help((
            'Show the introductory text that is displayed when starting the game.',
        ))

    def _exit(self, _: str) -> Optional[bool]:
        return True

    def _exit_help(self) -> None:
        self.print_help((
            'Exit the game.',
        ))

    def _go(self, exit_: str) -> Optional[bool]:
        if exit_ in self.current_room.exits:
            exit_data = self.current_room.exits.get(exit_)

            if isinstance(exit_data, ItemConditionedExit):
                exit_data = exit_data.exit_()

            if isinstance(exit_data, Room):
                self.current_room = exit_data

                self.line(self.current_room.look())
            elif isinstance(exit_data, GameOverExit):
                self.line(exit_data.text)

                return True
            elif isinstance(exit_data, TextExit):
                self.line(exit_data.text)

                if exit_data.exit:
                    self.current_room = exit_data.exit

                    self.line('')
                    self.line(self.current_room.look())
        else:
            self.line('I don\'t understand; try \'help\' for instructions.')

        return

    def _go_help(self) -> None:
        self.print_help((
            'go <exit> or merely <exit>',
            '',
            'Travel to the direction <exit>.',
        ))

    def _inv(self, _: str) -> Optional[bool]:
        self.line(self.inventory.look())

        return

    def _inv_help(self) -> None:
        self.print_help((
            'List items currently in inventory.',
        ))

    def _take(self, item_identifier: str) -> Optional[bool]:
        if self.current_room.take_item(item_identifier):
            self.line('Taken.')
        else:
            self.line('You see no such item.')

        return

    def _take_help(self) -> None:
        self.print_help((
            'take <item>',
            '',
            'Take item <item> from the current room and put it into the inventory.',
        ))

    def _drop(self, item_identifier: str) -> Optional[bool]:
        if self.inventory.drop(item_identifier):
            self.line('Dropped.')
        else:
            self.line('You can\'t find that in your pack.')

        return

    def _drop_help(self) -> None:
        self.print_help((
            'drop <item>',
            '',
            'Remove the item <item> from the inventory and drop it into the current room.',
        ))

    def _use(self, item_identifier: str) -> Optional[bool]:
        if not self.inventory.use(item_identifier):
            self.line('You can\'t find that in your pack.')

        return

    def _use_help(self) -> None:
        self.print_help((
            'use <item>',
            '',
            'Activate or apply item <item>. Item must be present in inventory.',
        ))

    def _spawn(self, item_identifier: str) -> Optional[bool]:
        if self.inventory.spawn(item_identifier):
            self.line('Spawned.')
        else:
            self.line('Unknown item.')

        return

    def _spawn_help(self) -> None:
        self.print_help((
            'spawn <item>',
            '',
            'Debug: Spawn a new item identified by <item> into the player’s inventory.',
        ))

    def _destroy(self, item_identifier: str) -> Optional[bool]:
        if self.inventory.destroy(item_identifier):
            self.line('Destroyed.')
        else:
            self.line('Unknown item.')

        return

    def _destroy_help(self) -> None:
        self.print_help((
            'destroy <item>',
            '',
            'Debug: Destroy item identified by <item> in player’s inventory.',
        ))

    def _tp(self, room_identifier: str) -> Optional[bool]:
        if room_identifier not in self.world.rooms:
            self.line('Unknown room.')

            return

        self.current_room = self.world.rooms.get(room_identifier)

        self.line(self.current_room.look())

        return

    def _tp_help(self) -> None:
        self.print_help((
            'tp <room>',
            '',
            'Debug: Teleport the player to the room identified by <room>.',
        ))

    def default(self, line: str) -> Optional[bool]:
        return self._go(line)


__all__ = [
    'Game',
]
