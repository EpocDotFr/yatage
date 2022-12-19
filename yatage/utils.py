from yatage.world import Item, List
from typing import Optional


def get_item(items_list: List[Item], item_identifier: str) -> Optional[Item]:
    return next(
        (item for item in items_list if item.definition.identifier == item_identifier),
        None
    )
