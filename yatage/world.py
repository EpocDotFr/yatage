from yatage.item import ItemDefinition, ItemUse, ItemConditionedUse, ItemConditions
from typing import Dict, Optional, Any, Union
from yatage.room import Room
import dataclasses
import yaml


@dataclasses.dataclass
class ItemConditionedExit:
    conditions: ItemConditions
    success: Room
    failure: Room

    def do_exit(self) -> Room:
        return self.success if self.conditions.are_met() else self.failure


@dataclasses.dataclass
class GameOverExit:
    text: str


@dataclasses.dataclass
class World:
    game: Any  # TODO Typing
    version: int
    name: str
    start: Optional[Room] = None
    rooms: Dict[str, Room] = dataclasses.field(default_factory=dict)
    items: Dict[str, ItemDefinition] = dataclasses.field(default_factory=dict)
    description: Optional[str] = None
    author: Optional[str] = None

    @classmethod
    def load(cls, game):  # TODO Typing
        with open(game.world_filename, 'rb') as f:
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
        self.description = world_data.get('description')
        self.author = world_data.get('author')

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
            exits = {}

            for exit_name, exit_data in exits_data.items():
                exit_ = None

                if isinstance(exit_data, str):
                    exit_ = self.rooms.get(exit_data)
                elif isinstance(exit_data, dict):
                    if 'conditions' in exit_data:
                        conditions = exit_data.get('conditions')

                        exit_ = ItemConditionedExit(
                            ItemConditions(
                                self,
                                conditions.get('has', []),
                                conditions.get('has_not', [])
                            ),
                            self.rooms.get(exit_data.get('success')),
                            self.rooms.get(exit_data.get('failure'))
                        )
                    elif 'game_over' in exit_data:
                        exit_ = GameOverExit(
                            exit_data.get('game_over')
                        )

                if not exit_:
                    continue

                exits[exit_name] = exit_

            self.rooms.get(room_identifier).exits = exits

    def load_items(self, world_data: dict) -> None:
        for item_identifier, item_data in world_data.get('items').items():
            self.items[item_identifier] = ItemDefinition(
                self,
                item_identifier,
                item_data.get('look')
            )

    def load_items_uses(self, world_data: dict) -> None:
        for item_identifier, item_data in world_data.get('items').items():
            use_data = item_data.get('use')
            use = self.load_item_use_or_str(use_data)

            if not use:
                use = self.load_item_conditioned_use(use_data)

            self.items.get(item_identifier).use = use

    def load_item_use_or_str(self, use_data: Union[str, Dict]) -> Optional[Union[str, ItemUse]]:
        if isinstance(use_data, str):
            return use_data
        elif isinstance(use_data, dict) and 'text' in use_data:
            return ItemUse(
                self,
                use_data.get('text'),
                use_data.get('remove', []),
                use_data.get('spawn', [])
            )

        return None

    def load_item_conditioned_use(self, use_data: Union[str, Dict]) -> Optional[Union[str, ItemConditionedUse]]:
        if isinstance(use_data, dict) and 'conditions' in use_data:
            conditions = use_data.get('conditions')

            return ItemConditionedUse(
                ItemConditions(
                    self,
                    conditions.get('has', []),
                    conditions.get('has_not', [])
                ),
                self.load_item_use_or_str(use_data.get('success')),
                self.load_item_use_or_str(use_data.get('failure'))
            )

        return None


__all__ = [
    'World',
    'GameOverExit',
    'ItemConditionedExit',
]
