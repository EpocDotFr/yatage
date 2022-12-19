from typing import List


def get_item(items_list: List, item_identifier: str):  # TODO Typing
    return next(
        (item for item in items_list if item.definition.identifier == item_identifier),
        None
    )
