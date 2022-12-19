from typing import Dict, Optional, Union, List, Any
import dataclasses
import yaml


@dataclasses.dataclass
class ItemUse:
    definition: Any # TODO Typing
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
    definition: Any # TODO Typing
    conditions: List # TODO Typing
    success: Optional[Union[str, ItemUse]] = None
    failure: Optional[Union[str, ItemUse]] = None

    def do_use(self, item_instance) -> Optional[str]: # TODO Typing
        pass


@dataclasses.dataclass
class ItemDefinition:
    world: Any # TODO Typing
    identifier: str
    look: str
    use: Optional[Union[str, ItemUse, ItemConditionedUse]] = None

    def create_item(self): # TODO Typing
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


@dataclasses.dataclass
class Room:
    world: Any # TODO Typing
    identifier: str
    description: str
    name: Optional[str]
    items: List[Item] = dataclasses.field(default_factory=list)
    exits: Dict[str, Any] = dataclasses.field(default_factory=dict) # TODO Typing

    def do_look(self) -> str:
        text = [
            f'== {self.name or self.identifier} ==',
        ]

        if self.description:
            text.append(self.description)

        if self.items:
            text.extend((
                '',
                'Things of interest here:',
            ))

            for item in self.items:
                text.append(f'- {item.definition.identifier}')

        if self.exits:
            text.extend((
                '',
                f'There are {len(self.exits)} exits:',
            ))

            for exit_name in self.exits.keys():
                text.append(f'- {exit_name}')

        return '\n'.join(text)


@dataclasses.dataclass
class World:
    game: Any # TODO Typing
    version: int
    name: str
    start: Optional[Room] = None
    rooms: Dict[str, Room] = dataclasses.field(default_factory=dict)
    items: Dict[str, ItemDefinition] = dataclasses.field(default_factory=dict)
    description: str = ''
    author: str = ''

    @classmethod
    def load(cls, game, world_filename: str): # TODO Typing
        with open(world_filename, 'rb') as f:
            world_data = yaml.safe_load(f) # TODO Move to stream-based loading?

        ret = cls(
            game,
            world_data.get('version'),
            world_data.get('name')
        )

        ret.load_metadata(world_data)

        ret.load_items(world_data)
        ret.load_items_uses(world_data)

        ret.load_rooms(world_data)
        ret.load_rooms_exits(world_data)

        ret.start = ret.rooms.get(world_data.get('start'))

        return ret

    def load_metadata(self, world_data: dict) -> None:
        self.description = world_data.get('description', '')
        self.author = world_data.get('author', '')

    def load_rooms(self, world_data: dict) -> None:
        for room_identifier, room_data in world_data.get('rooms').items():
            items = [
                self.items.get(item_identifier).create_item() for item_identifier in room_data.get('items', [])
            ]

            self.rooms[room_identifier] = Room(
                self,
                room_identifier,
                room_data.get('description', ''),
                room_data.get('name'),
                items
            )

    def load_rooms_exits(self, world_data: dict) -> None:
        for room_identifier, room_data in world_data.get('rooms').items():
            exits_data = room_data.get('exits', {})

            self.rooms.get(room_identifier).exits = {
                exit_name: self.rooms.get(exit_identifier) for exit_name, exit_identifier in exits_data.items() if isinstance(exit_identifier, str) # TODO handle conditional exits
            }

    def load_items(self, world_data: dict) -> None:
        for item_identifier, item_data in world_data.get('items').items():
            self.items[item_identifier] = ItemDefinition(
                self,
                item_identifier,
                item_data.get('look')
            )

    def load_items_uses(self, world_data: dict) -> None:
        for item_identifier, item_data in world_data.get('items').items():
            use = None

            use_data = item_data.get('use')

            if isinstance(use_data, str):
                use = use_data
            elif isinstance(use_data, dict):
                if 'text' in use_data:
                    use = ItemUse(
                        self.items.get(item_identifier),
                        use_data.get('text'),
                        use_data.get('remove', []),
                        use_data.get('spawn', [])
                    )

            self.items.get(item_identifier).use = use

