from typing import Optional, List, Any, Union
import dataclasses


@dataclasses.dataclass
class ItemUse:
    world: Any  # TODO Typing
    text: str
    remove: Optional[List[str]] = dataclasses.field(default_factory=list)
    spawn: Optional[List[str]] = dataclasses.field(default_factory=list)
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
    has: Optional[List[str]] = dataclasses.field(default_factory=list)
    has_not: Optional[List[str]] = dataclasses.field(default_factory=list)

    def are_met(self) -> bool:
        results = []

        results.extend([
            self.world.game.inventory.has(item_identifier) for item_identifier in self.has
        ])

        results.extend([
            not self.world.game.inventory.has(item_identifier) for item_identifier in self.has_not
        ])

        return False not in results

    def __str__(self) -> str:
        conditions = ''

        if self.has:
            conditions += 'has {}'.format(', '.join(self.has))

        if self.has and self.has_not:
            conditions += ' and '

        if self.has_not:
            conditions += 'has not {}'.format(', '.join(self.has_not))

        return conditions


@dataclasses.dataclass
class ItemDefinition:
    world: Any  # TODO Typing
    identifier: str
    look: str
    use: Optional[Union[str, ItemUse, ItemConditionedUse]] = None

    def create_item(self):  # TODO Typing
        return Item(self)


@dataclasses.dataclass
class Item:
    definition: ItemDefinition

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
