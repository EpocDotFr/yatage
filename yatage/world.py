from yatage.item import ItemDefinition, ItemUse, ItemConditionedUse, ItemConditions, RoomConditions
from typing import Dict, Optional, Any, Union
from yatage.room import Room
import dataclasses
import yaml


@dataclasses.dataclass
class ItemConditionedExit:
    conditions: ItemConditions
    success: Any  # TODO Typing
    failure: Any  # TODO Typing

    def do_exit(self) -> Room:
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
    exit: Optional[Room] = None

    def __str__(self) -> str:
        text = 'Text'

        if self.exit:
            text += f' then {self.exit}'

        return text


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
        ret.load_rooms(world_data)
        ret.load_rooms_exits(world_data)
        ret.load_items_uses(world_data)

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
                exit_ = self.load_room_exit_room_or_game_over_or_text(exit_data)

                if not exit_:
                    exit_ = self.load_room_item_conditioned_exit(exit_data)

                if not exit_:
                    continue

                exits[exit_name] = exit_

            self.rooms.get(room_identifier).exits = exits

    def load_room_exit_room_or_game_over_or_text(self, exit_data: Union[str, Dict]) -> Optional[Union[Room, GameOverExit, TextExit]]:
        if isinstance(exit_data, str):
            return self.rooms.get(exit_data)
        elif isinstance(exit_data, dict):
            if 'game_over' in exit_data:
                return GameOverExit(
                    exit_data.get('game_over')
                )
            elif 'text' in exit_data:
                return TextExit(
                    exit_data.get('text'),
                    self.rooms.get(exit_data.get('exit')) if 'exit' in exit_data else None
                )

        return None

    def load_room_item_conditioned_exit(self, exit_data: Union[str, Dict]) -> Optional[ItemConditionedExit]:
        if isinstance(exit_data, dict) and 'items_conditions' in exit_data:
            items_conditions = exit_data.get('items_conditions')

            return ItemConditionedExit(
                ItemConditions(
                    self,
                    items_conditions.get('has', []),
                    items_conditions.get('has_not', []),
                    items_conditions.get('has_used', []),
                    items_conditions.get('has_not_used', [])
                ),
                self.load_room_exit_room_or_game_over_or_text(exit_data.get('success')) if 'success' in exit_data else None,
                self.load_room_exit_room_or_game_over_or_text(exit_data.get('failure')) if 'failure' in exit_data else None
            )

        return None

    def load_items(self, world_data: dict) -> None:
        for item_identifier, item_data in world_data.get('items').items():
            self.items[item_identifier] = ItemDefinition(
                self,
                item_identifier,
                item_data.get('look'),
                alias=item_data.get('alias')
            )

    def load_items_uses(self, world_data: dict) -> None:
        for item_identifier, item_data in world_data.get('items').items():
            use_data = item_data.get('use')
            use = self.load_item_use_or_str(use_data)

            if not use:
                use = self.load_item_or_room_conditioned_use(use_data)

            if not use:
                continue

            self.items.get(item_identifier).use = use

    def load_item_use_or_str(self, use_data: Union[str, Dict]) -> Optional[Union[str, ItemUse]]:
        if isinstance(use_data, str):
            return use_data
        elif isinstance(use_data, dict) and 'text' in use_data:
            return ItemUse(
                self,
                use_data.get('text'),
                use_data.get('remove', []),
                use_data.get('spawn', []),
                use_data.get('mark_used', []),
                self.rooms.get(use_data.get('teleport')) if 'teleport' in use_data else None
            )

        return None

    def load_item_or_room_conditioned_use(self, use_data: Union[str, Dict]) -> Optional[ItemConditionedUse]:
        if isinstance(use_data, dict):
            if 'items_conditions' in use_data:
                items_conditions = use_data.get('items_conditions')

                conditions = ItemConditions(
                    self,
                    items_conditions.get('has', []),
                    items_conditions.get('has_not', []),
                    items_conditions.get('has_used', []),
                    items_conditions.get('has_not_used', [])
                )
            elif 'room_conditions' in use_data:
                room_conditions = use_data.get('room_conditions')

                conditions = RoomConditions(
                    self,
                    room_conditions.get('in', []),
                    room_conditions.get('not_in', []),
                )
            else:
                return None

            return ItemConditionedUse(
                conditions,
                self.load_item_use_or_str(use_data.get('success')) if 'success' in use_data else None,
                self.load_item_use_or_str(use_data.get('failure')) if 'failure' in use_data else None
            )

        return None


__all__ = [
    'ItemConditionedExit',
    'GameOverExit',
    'TextExit',
    'World',
]
