from typing import Optional, List, Any, Dict
from yatage.item import Item
import dataclasses


@dataclasses.dataclass
class ItemConditionedExit:
    conditions: Any  # TODO Typing
    success: Any  # TODO Typing
    failure: Any  # TODO Typing

    def do_exit(self):  # TODO Typing
        return self.success if self.conditions.are_met() else self.failure

    def __str__(self) -> str:
        return f'{self.success} if ({self.conditions}) or {self.failure}'


@dataclasses.dataclass
class GameOverExit:
    text: str

    def __str__(self) -> str:
        return 'Text then game over'


@dataclasses.dataclass
class TextExit:
    text: str
    exit: Optional[Any] = None  # TODO Typing

    def __str__(self) -> str:
        text = 'Text'

        if self.exit:
            text += f' then {self.exit}'

        return text


@dataclasses.dataclass
class Room:
    world: Any  # TODO Typing
    identifier: str
    description: str
    name: Optional[str] = None
    items: List[Item] = dataclasses.field(default_factory=list)
    exits: Dict[str, Any] = dataclasses.field(default_factory=dict)  # TODO Typing

    def do_look(self) -> str:
        name = str(self)
        header = '*' * len(name)

        text = [
            header,
            name,
            header,
            '',
        ]

        if self.description:
            text.append(self.description)

        if self.items:
            text.extend((
                '',
                'Things of interest here:',
                '------------------------',
            ))

            for item in self.items:
                text.append(f'  - {item.definition.alias_or_identifier}')

        if self.exits:
            exits_text = f'There are {len(self.exits)} exits:'

            text.extend((
                '',
                exits_text,
                '-' * len(exits_text),
            ))

            for exit_name, exit_ in self.exits.items():
                if self.world.game.debug:
                    exit_name += f' ({exit_})'

                text.append(f'  - {exit_name}')

        return '\n'.join(text)

    @property
    def name_or_identifier(self) -> str:
        return self.name or self.identifier

    def __str__(self) -> str:
        name = self.name_or_identifier

        if self.world.game.debug and self.name and self.name != self.identifier:
            name += f' [{self.identifier}]'

        return name


__all__ = [
    'ItemConditionedExit',
    'GameOverExit',
    'TextExit',
    'Room',
]
