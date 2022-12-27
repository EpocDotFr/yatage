from __future__ import annotations
from yatage.item import ItemDefinition, ItemUse, ItemConditionedUse, ItemConditions, RoomConditions
from yatage.room import Room, GameOverExit, TextExit, ItemConditionedExit
from typing import Dict, Optional, Any, Union, Tuple
from yatage.exceptions import WorldReadError
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
    description: Optional[str] = None
    author: Optional[str] = None

    SUPPORTED_VERSIONS: Tuple[int] = (1,)

    @classmethod
    def load(cls, game) -> World:  # TODO Typing
        with open(game.world_filename, 'rb') as f:
            world_data = yaml.safe_load(f)  # TODO Move to stream-based loading?

        version = world_data.get('version')

        if not version:
            raise WorldReadError('Top level "version" is required')
        elif not isinstance(version, int):
            raise WorldReadError('Top level "version" must be an integer')
        elif version not in World.SUPPORTED_VERSIONS:
            raise WorldReadError('Invalid top level "version"')

        name = world_data.get('name')

        if not name:
            raise WorldReadError('Top level "name" is required')
        elif not isinstance(name, str):
            raise WorldReadError('Top level "name" must be a string')

        start = world_data.get('start')

        if not start:
            raise WorldReadError('Top level "start" is required')
        elif not isinstance(start, str):
            raise WorldReadError('Top level "start" must be a string')

        ret = cls(
            game,
            version,
            name
        )

        description = world_data.get('description')

        if description and not isinstance(description, str):
            raise WorldReadError('Top level "description" must be a string')

        ret.description = description

        author = world_data.get('author')

        if author and not isinstance(author, str):
            raise WorldReadError('Top level "description" must be a string')

        ret.author = author

        items_data = world_data.get('items', {})

        if not isinstance(items_data, dict):
            raise WorldReadError('Invalid top level "items": must be a map')

        ret.load_items(items_data)

        rooms_data = world_data.get('rooms', {})

        if not rooms_data:
            raise WorldReadError('Top level "rooms" is required and must contain at least one valid room')
        elif not isinstance(rooms_data, dict):
            raise WorldReadError('Invalid top level "rooms": must be a map')

        ret.load_rooms(rooms_data)
        ret.load_rooms_exits(rooms_data)
        ret.load_items_uses(items_data)

        if start not in ret.rooms:
            raise WorldReadError('Invalid top level "start": room not found')

        ret.start = ret.rooms.get(start)

        return ret

    def load_rooms(self, rooms_data: dict) -> None:
        for room_identifier, room_data in rooms_data.items():
            items_data = room_data.get('items', [])

            if not isinstance(items_data, list):
                raise WorldReadError(f'Invalid "items" in room "{room_identifier}": must be an array')

            items = []

            for item_identifier in items_data:
                if item_identifier not in self.items:
                    raise WorldReadError(f'Item "{item_identifier}" in room "{room_identifier}" does not exist')

                items.append(self.items.get(item_identifier).create_item())

            description = room_data.get('description')

            if not description:
                raise WorldReadError(f'"description" is missing in room "{room_identifier}"')
            elif not isinstance(description, str):
                raise WorldReadError(f'"description" in room "{room_identifier}" must be a string')

            name = room_data.get('name')

            if name and not isinstance(name, str):
                raise WorldReadError(f'"name" in room "{room_identifier}" must be a string')

            self.rooms[room_identifier] = Room(
                self,
                room_identifier,
                description,
                name,
                items
            )

    def load_rooms_exits(self, rooms_data: dict) -> None:
        for room_identifier, room_data in rooms_data.items():
            if 'exits' not in room_data:
                continue

            exits_data = room_data.get('exits', {})

            if not isinstance(exits_data, dict):
                raise WorldReadError(f'Invalid "exits" in room "{room_identifier}": must be a map')

            exits = {}

            for exit_name, exit_data in exits_data.items():
                exit_ = self.load_room_exit_room_or_game_over_or_text(exit_data) or self.load_room_item_conditioned_exit(exit_data)

                if not exit_:
                    raise WorldReadError(f'Invalid exit "{exit_name}" in room "{room_identifier}": unknown exit type')

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

    def load_items(self, items_data: dict) -> None:
        for item_identifier, item_data in items_data.items():
            look = item_data.get('look')

            if not look:
                raise WorldReadError(f'"look" is missing in item "{item_identifier}"')
            elif not isinstance(look, str):
                raise WorldReadError(f'"look" in item "{item_identifier}" must be a string')

            alias = item_data.get('alias')

            if alias and not isinstance(alias, str):
                raise WorldReadError(f'"alias" in item "{item_identifier}" must be a string')

            self.items[item_identifier] = ItemDefinition(
                self,
                item_identifier,
                look,
                alias=alias
            )

        for item in self.items.values():
            if not item.alias:
                continue

            items_aliases = {
                item_for_alias.alias: item_for_alias.identifier for item_for_alias in self.items.values() if item_for_alias.alias and item_for_alias.identifier != item.identifier
            }

            if item.alias in items_aliases:
                used_by = items_aliases.get(item.alias)

                raise WorldReadError(f'Alias "{item.alias}" in item "{item.identifier}" is already in use by item "{used_by}"')

    def load_items_uses(self, items_data: dict) -> None:
        for item_identifier, item_data in items_data.items():
            if 'use' not in item_data:
                continue

            use_data = item_data.get('use')
            use = self.load_item_use_or_str(use_data) or self.load_item_or_room_conditioned_use(use_data)

            if not use:
                raise WorldReadError(f'Invalid "use" in item "{item_identifier}": unknown use type')

            self.items.get(item_identifier).use = use

    def load_item_use_or_str(self, use_data: Union[str, Dict]) -> Optional[Union[str, ItemUse]]:
        if isinstance(use_data, str):
            return use_data

        if isinstance(use_data, dict) and 'text' in use_data:
            text = use_data.get('text')

            if not text:
                raise WorldReadError(f'"text" is missing in "use"')  # TODO Elaborate
            elif not isinstance(text, str):
                raise WorldReadError(f'"text" in "use" must be a string')  # TODO Elaborate

            remove = use_data.get('remove', [])

            if not isinstance(remove, list):
                raise WorldReadError(f'Invalid "remove" in "use": must be an array')  # TODO Elaborate

            spawn = use_data.get('spawn', [])

            if not isinstance(spawn, list):
                raise WorldReadError(f'Invalid "spawn" in "use": must be an array')  # TODO Elaborate

            mark_used = use_data.get('mark_used', [])

            if not isinstance(mark_used, list):
                raise WorldReadError(f'Invalid "mark_used" in "use": must be an array')  # TODO Elaborate

            teleport = use_data.get('teleport')

            if teleport:
                if not isinstance(teleport, str):
                    raise WorldReadError(f'"teleport" in "use" must be a string')  # TODO Elaborate
                elif teleport not in self.rooms:
                    raise WorldReadError('Invalid "teleport" in "use": room not found')  # TODO Elaborate

            return ItemUse(
                self,
                text,
                remove,
                spawn,
                mark_used,
                self.rooms.get(teleport) if teleport else None
            )

        return None

    def load_item_or_room_conditioned_use(self, use_data: Union[str, Dict]) -> Optional[ItemConditionedUse]:
        if not isinstance(use_data, dict):
            return None

        conditions = None

        if 'items_conditions' in use_data:
            items_conditions = use_data.get('items_conditions', {})

            if not isinstance(items_conditions, dict):
                raise WorldReadError(f'Invalid "items_conditions" in "use": must be a map')  # TODO Elaborate

            conditions = ItemConditions(
                self,
                items_conditions.get('has', []),
                items_conditions.get('has_not', []),
                items_conditions.get('has_used', []),
                items_conditions.get('has_not_used', [])
            )
        elif 'room_conditions' in use_data:
            room_conditions = use_data.get('room_conditions', {})

            if not isinstance(room_conditions, dict):
                raise WorldReadError(f'Invalid "room_conditions" in "use": must be a map')  # TODO Elaborate

            conditions = RoomConditions(
                self,
                room_conditions.get('in', []),
                room_conditions.get('not_in', []),
            )

        if conditions:
            return ItemConditionedUse(
                conditions,
                self.load_item_use_or_str(use_data.get('success')) if 'success' in use_data else None,
                self.load_item_use_or_str(use_data.get('failure')) if 'failure' in use_data else None
            )

        return None


__all__ = [
    'World',
]
