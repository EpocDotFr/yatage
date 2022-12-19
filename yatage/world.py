from yatage.item import ItemDefinition, ItemUse
from typing import Dict, Optional, Any
from yatage.room import Room
import dataclasses
import yaml


@dataclasses.dataclass
class World:
    game: Any  # TODO Typing
    version: int
    name: str
    start: Optional[Room] = None
    rooms: Dict[str, Room] = dataclasses.field(default_factory=dict)
    items: Dict[str, ItemDefinition] = dataclasses.field(default_factory=dict)
    description: str = ''
    author: str = ''

    @classmethod
    def load(cls, game, world_filename: str):  # TODO Typing
        with open(world_filename, 'rb') as f:
            world_data = yaml.safe_load(f)  # TODO Move to stream-based loading?

        ret = cls(
            game,
            world_data.get('version'),
            world_data.get('name')
        )

        ret.load_metadata(world_data)

        ret.load_items(world_data)
        ret.load_items_uses(world_data)

        ret.load_rooms(world_data)
        ret.load_rooms_exits(world_data)

        ret.start = ret.rooms.get(world_data.get('start'))

        return ret

    def load_metadata(self, world_data: dict) -> None:
        self.description = world_data.get('description', '')
        self.author = world_data.get('author', '')

    def load_rooms(self, world_data: dict) -> None:
        for room_identifier, room_data in world_data.get('rooms').items():
            items = [
                self.items.get(item_identifier).create_item() for item_identifier in room_data.get('items', [])
            ]

            self.rooms[room_identifier] = Room(
                self,
                room_identifier,
                room_data.get('description', ''),
                room_data.get('name'),
                items
            )

    def load_rooms_exits(self, world_data: dict) -> None:
        for room_identifier, room_data in world_data.get('rooms').items():
            exits_data = room_data.get('exits', {})

            self.rooms.get(room_identifier).exits = {
                exit_name: self.rooms.get(exit_identifier) for exit_name, exit_identifier in exits_data.items() if
                isinstance(exit_identifier, str)  # TODO handle conditional exits
            }

    def load_items(self, world_data: dict) -> None:
        for item_identifier, item_data in world_data.get('items').items():
            self.items[item_identifier] = ItemDefinition(
                self,
                item_identifier,
                item_data.get('look')
            )

    def load_items_uses(self, world_data: dict) -> None:
        for item_identifier, item_data in world_data.get('items').items():
            use = None

            use_data = item_data.get('use')

            if isinstance(use_data, str):
                use = use_data
            elif isinstance(use_data, dict):
                if 'text' in use_data:
                    use = ItemUse(
                        self.items.get(item_identifier),
                        use_data.get('text'),
                        use_data.get('remove', []),
                        use_data.get('spawn', [])
                    )

            self.items.get(item_identifier).use = use


__all__ = [
    'World',
]
