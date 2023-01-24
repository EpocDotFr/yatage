from typing import Optional, List, Any, Union
import dataclasses


@dataclasses.dataclass
class ItemUse:
    world: Any  # TODO Typing
    text: str
    remove: List[str] = dataclasses.field(default_factory=list)
    spawn: List[str] = dataclasses.field(default_factory=list)
    mark_used: List[str] = dataclasses.field(default_factory=list)
    teleport: Optional[Any] = None  # TODO Typing

    def use(self, item_instance) -> str:  # TODO Typing
        for item_identifier in self.remove:
            self.world.game.inventory.destroy(
                item_instance.definition.identifier if item_identifier == 'self' else item_identifier
            )

        for item_identifier in self.spawn:
            self.world.game.inventory.append(
                self.world.items.get(item_identifier).create_item()
            )

        for item_identifier in self.mark_used:
            item = self.world.game.inventory.get(
                item_instance.definition.identifier if item_identifier == 'self' else item_identifier
            )

            if item:
                item.used = True

        return self.text


@dataclasses.dataclass
class ItemConditionedUse:
    conditions: Any  # TODO Typing
    success: Union[str, ItemUse]
    failure: Union[str, ItemUse]

    def use(self, item_instance) -> Optional[str]:  # TODO Typing
        result_attr = self.success if self.conditions.are_met() else self.failure

        if isinstance(result_attr, str):
            return result_attr
        elif isinstance(result_attr, ItemUse):
            return result_attr.use(item_instance)

        return None


@dataclasses.dataclass
class RoomConditions:
    world: Any  # TODO Typing
    in_: List[str] = dataclasses.field(default_factory=list)
    not_in: List[str] = dataclasses.field(default_factory=list)

    def are_met(self) -> bool:
        results = []

        results.extend([
            self.world.game.current_room == self.world.rooms.get(room_identifier) for room_identifier in self.in_ if room_identifier in self.world.rooms
        ])

        results.extend([
            not self.world.game.current_room == self.world.rooms.get(room_identifier) for room_identifier in self.not_in if room_identifier in self.world.rooms
        ])

        return False not in results

    def __str__(self) -> str:
        conditions = []

        if self.in_:
            conditions.append('in {}'.format(', '.join(self.in_)))

        if self.not_in:
            conditions.append('not in {}'.format(', '.join(self.not_in)))

        return ' and '.join(conditions)


@dataclasses.dataclass
class ItemConditions:
    world: Any  # TODO Typing
    has: List[str] = dataclasses.field(default_factory=list)
    has_not: List[str] = dataclasses.field(default_factory=list)
    has_used: List[str] = dataclasses.field(default_factory=list)
    has_not_used: List[str] = dataclasses.field(default_factory=list)

    def are_met(self) -> bool:
        results = []

        results.extend([
            self.world.game.inventory.has(item_identifier) for item_identifier in self.has
        ])

        results.extend([
            not self.world.game.inventory.has(item_identifier) for item_identifier in self.has_not
        ])

        results.extend([
            self.world.game.inventory.get(item_identifier).used for item_identifier in self.has_used if self.world.game.inventory.has(item_identifier)
        ])

        results.extend([
            not self.world.game.inventory.get(item_identifier).used for item_identifier in self.has_not_used if self.world.game.inventory.has(item_identifier)
        ])

        return False not in results

    def __str__(self) -> str:
        conditions = []

        if self.has:
            conditions.append('has {}'.format(', '.join(self.has)))

        if self.has_not:
            conditions.append('has not {}'.format(', '.join(self.has_not)))

        if self.has_used:
            conditions.append('has used {}'.format(', '.join(self.has_used)))

        if self.has_not_used:
            conditions.append('has not used {}'.format(', '.join(self.has_not_used)))

        return ' and '.join(conditions)


@dataclasses.dataclass
class ItemDefinition:
    world: Any  # TODO Typing
    identifier: str
    look: str
    use: Optional[Union[str, ItemUse, ItemConditionedUse]] = None
    alias: Optional[str] = None

    def create_item(self):  # TODO Typing
        return Item(self)

    @property
    def alias_or_identifier(self) -> str:
        return self.alias or self.identifier


@dataclasses.dataclass
class Item:
    definition: ItemDefinition
    used: bool = False

    def use(self) -> None:
        if not self.definition.use:
            self.definition.world.game.line('This item does not seem to be usable.')

            return

        text = None

        if isinstance(self.definition.use, str):
            text = self.definition.use
        elif isinstance(self.definition.use, (ItemUse, ItemConditionedUse)):
            text = self.definition.use.use(self)

        if text:
            self.definition.world.game.line(text)

        if isinstance(self.definition.use, ItemUse) and self.definition.use.teleport:
            self.definition.world.game.current_room = self.definition.use.teleport

            self.definition.world.game.line(
                self.definition.world.game.current_room.look()
            )

    def look(self) -> str:
        return self.definition.look


__all__ = [
    'ItemUse',
    'ItemConditionedUse',
    'RoomConditions',
    'ItemConditions',
    'ItemDefinition',
    'Item',
]
