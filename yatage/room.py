from typing import Optional, List, Any, Dict
from yatage.item import Item
import dataclasses


@dataclasses.dataclass
class Room:
    world: Any  # TODO Typing
    identifier: str
    description: str
    name: Optional[str]
    items: List[Item] = dataclasses.field(default_factory=list)
    exits: Dict[str, Any] = dataclasses.field(default_factory=dict)  # TODO Typing

    def do_look(self) -> str:
        name = self.name or self.identifier

        text = [
            name,
            '-' * len(name),
            '',
        ]

        if self.description:
            text.append(self.description)

        if self.items:
            text.extend((
                '',
                'Things of interest here:',
            ))

            for item in self.items:
                text.append(f'- {item.definition.identifier}')

        if self.exits:
            text.extend((
                '',
                f'There are {len(self.exits)} exits:',
            ))

            for exit_name in self.exits.keys():
                text.append(f'- {exit_name}')

        return '\n'.join(text)


__all__ = [
    'Room',
]
