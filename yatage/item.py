from typing import Optional, List, Any, Union
import yatage.utils
import dataclasses


@dataclasses.dataclass
class ItemUse:
    world: Any  # TODO Typing
    text: str
    remove: List[str] = dataclasses.field(default_factory=list)
    spawn: List[str] = dataclasses.field(default_factory=list)
    mark_used: List[str] = dataclasses.field(default_factory=list)
    teleport: Optional[Any] = None  # TODO Typing

    def do_use(self, item_instance) -> str:
        for item_identifier in self.remove:
            self.world.game.inventory.destroy(
                item_instance.definition.identifier if item_identifier == 'self' else item_identifier
            )

        for item_identifier in self.spawn:
            self.world.game.inventory.append(
                self.world.items.get(item_identifier).create_item()
            )

        for item_identifier in self.mark_used:
            item = yatage.utils.get_item(
                self.world.game.inventory,
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

    def do_use(self, item_instance) -> Optional[str]:  # TODO Typing
        result_attr = self.success if self.conditions.are_met() else self.failure

        if isinstance(result_attr, str):
            return result_attr
        elif isinstance(result_attr, ItemUse):
            return result_attr.do_use(item_instance)

        return None


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
            yatage.utils.get_item(self.world.game.inventory, item_identifier).used for item_identifier in self.has_used if self.world.game.inventory.has(item_identifier)
        ])

        results.extend([
            not yatage.utils.get_item(self.world.game.inventory, item_identifier).used for item_identifier in self.has_not_used if self.world.game.inventory.has(item_identifier)
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

    def do_use(self) -> None:
        text = None

        if isinstance(self.definition.use, str):
            text = self.definition.use
        elif isinstance(self.definition.use, (ItemUse, ItemConditionedUse)):
            text = self.definition.use.do_use(self)

        if text:
            self.definition.world.game.line(text)

        if isinstance(self.definition.use, ItemUse) and self.definition.use.teleport:
            self.definition.world.game.current_room = self.definition.use.teleport

            self.definition.world.game.line(
                self.definition.world.game.current_room.do_look()
            )

    def do_look(self) -> str:
        return self.definition.look


__all__ = [
    'ItemUse',
    'ItemConditionedUse',
    'ItemConditions',
    'ItemDefinition',
    'Item',
]
