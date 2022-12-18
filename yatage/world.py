from typing import Dict, Optional, Union, List, Any
from copy import copy
import dataclasses
import yaml


@dataclasses.dataclass
class ItemUse:
    text: Optional[str]


@dataclasses.dataclass
class ItemDefinition:
    identifier: str
    look: str
    use: Optional[Union[str, ItemUse]] = None

    def create_item(self): # TODO Typing
        return Item(self)


@dataclasses.dataclass
class Item:
    definition: ItemDefinition


@dataclasses.dataclass
class Room:
    identifier: str
    description: str
    name: str
    items: List[Item] = dataclasses.field(default_factory=list)
    exits: Dict[str, Any] = dataclasses.field(default_factory=dict) # TODO Typing

    def textual(self) -> str:
        text = [
            '',
            '',
            f'== {self.name} ==',
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


@dataclasses.dataclass
class World:
    version: int
    name: str
    start: Optional[Room] = None
    rooms: Dict[str, Room] = dataclasses.field(default_factory=dict)
    items: Dict[str, ItemDefinition] = dataclasses.field(default_factory=dict)
    description: str = ''
    author: str = ''

    @classmethod
    def load(cls, world_filename: str): # TODO Typing
        with open(world_filename, 'rb') as f:
            world_data = yaml.safe_load(f) # TODO Move to stream-based loading?

        ret = cls(
            world_data.get('version'),
            world_data.get('name')
        )

        ret.load_metadata(world_data)
        ret.load_items(world_data)
        ret.load_rooms(world_data)

        return ret

    def load_metadata(self, world_data: dict) -> None:
        self.description = world_data.get('description', '')
        self.author = world_data.get('author', '')

    def load_rooms(self, world_data: dict) -> None:
        for room_identifier, room_data in world_data.get('rooms').items():
            self.rooms[room_identifier] = Room(
                room_identifier,
                room_data.get('description', ''),
                room_data.get('name', '') or room_identifier,
                [
                    self.items.get(item_identifier).create_item() for item_identifier in room_data.get('items', [])
                ],
                {
                    exit_name: self.rooms.get(exit_identifier) for exit_name, exit_identifier in room_data.get('exits', {}).items() if isinstance(exit_identifier, str) # TODO handle conditional exits
                }
            )

        self.start = self.rooms.get(world_data.get('start'))

    def load_items(self, world_data: dict) -> None:
        for item_identifier, item_data in world_data.get('items').items():
            use = None

            use_data = item_data.get('use')

            if isinstance(use_data, str):
                use = use_data
            elif isinstance(use_data, dict):
                use = ItemUse(
                    use_data.get('text')
                )

            self.items[item_identifier] = ItemDefinition(
                item_identifier,
                item_data.get('look'),
                use
            )
