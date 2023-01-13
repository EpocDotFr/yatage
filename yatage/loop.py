from typing import Tuple, List, Optional
from cmd import Cmd


class Loop(Cmd):
    prompt: str = '\nWhat do you do?\n===============\n> '
    doc_header: str = 'Available actions (type help <action>):'
    ruler: str = '^'
    hidden_commands: Tuple[str, ...] = ('do_EOF',)

    def postloop(self) -> None:
        self.line('')

    def precmd(self, line) -> str:
        self.line('')

        return line

    def do_EOF(self, _: str) -> Optional[bool]:
        return True

    def get_names(self) -> List:
        return [m for m in dir(self) if m not in self.hidden_commands]

    def line(self, text: str, end: str = '\n') -> None:
        self.stdout.write(f'{text}{end}')

    def print_help(self, lines: Tuple[str, ...]) -> None:
        self.line('\n'.join(lines))

    def run(self) -> None:
        try:
            self.cmdloop()
        except KeyboardInterrupt:
            pass


__all__ = [
    'Loop',
]
