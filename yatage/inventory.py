from collections import UserList
import yatage.utils


class Inventory(UserList):
    def __init__(self, game) -> None:  # TODO Typing
        super().__init__()

        self.game = game

    def look(self) -> str:
        text = [
            'Your inventory:',
            '---------------',
        ]

        for item in self:
            if not self.game.debug and item.used:
                continue

            name = item.definition.alias_or_identifier

            if self.game.debug:
                if item.used:
                    name += ' [used]'

                if item.definition.alias:
                    name += f' [alias of {item.definition.identifier}]'

            text.append(f'  - {name}')

        return '\n'.join(text)

    def get(self, item_identifier: str, attr: str = 'identifier'):  # TODO Typing
        return yatage.utils.get_item(self, item_identifier, attr)

    def has(self, item_identifier: str) -> bool:
        return True if self.get(item_identifier) else False

    def use(self, item_identifier: str) -> bool:
        item = self.get(item_identifier, 'alias_or_identifier')

        if not item:
            return False

        item.use()

        return True

    def drop(self, item_identifier: str) -> bool:
        item = self.get(item_identifier, 'alias_or_identifier')

        if not item:
            return False

        self.game.current_room.items.append(
            self.pop(
                self.index(item)
            )
        )

        return True

    def destroy(self, item_identifier: str) -> bool:
        item = self.get(item_identifier)

        if not item:
            return False

        self.remove(item)

        return True

    def spawn(self, item_identifier: str) -> bool:
        item_definition = self.game.world.items.get(item_identifier)

        if not item_definition:
            return False

        self.append(item_definition.create_item())

        return True


__all__ = [
    'Inventory',
]
