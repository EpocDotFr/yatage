from collections import UserList
from typing import List, Union


def get_item(items_list: Union[List, UserList], item_identifier: str, attr: str):  # TODO Typing
    return next(
        (item for item in items_list if getattr(item.definition, attr) == item_identifier),
        None
    )
