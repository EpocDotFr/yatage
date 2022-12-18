from typing import Dict, Optional
import dataclasses
import yaml


@dataclasses.dataclass
class Room:
    identifier: str
    description: str
    name: str


@dataclasses.dataclass
class Item:
    identifier: str
    look: str


@dataclasses.dataclass
class World:
    version: int
    name: str
    start: Optional[Room] = None
    rooms: Dict[str, Room] = dataclasses.field(default_factory=dict)
    items: Dict[str, Item] = dataclasses.field(default_factory=dict)
    description: str = None
    author: str = None

    @classmethod
    def load(cls, world_filename: str):
        with open(world_filename, 'rb') as f:
            world_data = yaml.safe_load(f)

        ret = cls(
            world_data.get('version'),
            world_data.get('name')
        )

        ret.load_metadata(world_data)
        ret.load_rooms(world_data)
        ret.load_items(world_data)

        return ret

    def load_metadata(self, world_data: dict) -> None:
        self.description = world_data.get('description')
        self.author = world_data.get('author')

    def load_rooms(self, world_data: dict) -> None:
        for identifier, room_data in world_data.get('rooms').items():
            self.rooms[identifier] = Room(
                identifier,
                room_data.get('description'),
                room_data.get('name') or identifier
            )

        self.start = self.rooms.get(world_data.get('start'))

    def load_items(self, world_data: dict) -> None:
        for identifier, item_data in world_data.get('items').items():
            self.items[identifier] = Item(
                identifier,
                item_data.get('look')
            )
