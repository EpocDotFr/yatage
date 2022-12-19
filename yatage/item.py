from typing import Optional, List, Any, Union
import dataclasses


@dataclasses.dataclass
class ItemUse:
    definition: Any  # TODO Typing
    text: str
    remove: Optional[List[str]] = dataclasses.field(default_factory=list)
    spawn: Optional[List[str]] = dataclasses.field(default_factory=list)

    def do_use(self, item_instance) -> Optional[str]:
        for item_identifier in self.remove:
            self.definition.world.game.inventory.destroy(
                item_instance.definition.identifier if item_identifier == 'self' else item_identifier
            )

        for item_identifier in self.spawn:
            self.definition.world.game.inventory.append(
                self.definition.world.items.get(item_identifier).create_item()
            )

        return self.text


@dataclasses.dataclass
class ItemConditionedUse:
    definition: Any  # TODO Typing
    conditions: List  # TODO Typing
    success: Optional[Union[str, ItemUse]] = None
    failure: Optional[Union[str, ItemUse]] = None

    def do_use(self, item_instance) -> Optional[str]:  # TODO Typing
        pass


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

    def do_use(self) -> Optional[str]:
        if isinstance(self.definition.use, str):
            return self.definition.use
        elif isinstance(self.definition.use, (ItemUse, ItemConditionedUse)):
            return self.definition.use.do_use(self)

        return None

    def do_look(self) -> str:
        return self.definition.look


__all__ = [
    'ItemUse',
    'ItemConditionedUse',
    'ItemDefinition',
    'Item',
]
