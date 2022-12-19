from collections import UserList
import yatage.utils


class Inventory(UserList):
    def __init__(self, game) -> None:  # TODO Typing
        super().__init__()

        self.game = game

    def do_look(self) -> str:
        text = [
            'Your inventory:',
        ]

        for item in self:
            text.append(f'- {item.definition.identifier}')

        return '\n'.join(text)

    def take(self, item_identifier: str) -> bool:
        item = yatage.utils.get_item(self.game.current_room.items, item_identifier)

        if not item:
            return False

        self.append(
            self.game.current_room.items.pop(
                self.game.current_room.items.index(item)
            )
        )

        return True

    def drop(self, item_identifier: str) -> bool:
        item = yatage.utils.get_item(self, item_identifier)

        if not item:
            return False

        self.game.current_room.items.append(
            self.pop(
                self.index(item)
            )
        )

        return True

    def destroy(self, item_identifier: str) -> bool:
        item = yatage.utils.get_item(self, item_identifier)

        if not item:
            return False

        self.remove(item)

        return True


__all__ = [
    'Inventory',
]
