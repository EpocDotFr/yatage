from marshmallow import Schema, fields, validate, EXCLUDE
from yatage.world import World


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class RoomSchema(BaseSchema):
    # items = fields.List(fields.Dict())
    description = fields.String(required=True)
    name = fields.String()


class TextExitSchema(BaseSchema):
    pass


class GameOverExitSchema(BaseSchema):
    pass


class ItemConditionedExitSchema(BaseSchema):
    pass


class ItemSchema(BaseSchema):
    look = fields.String(required=True)
    alias = fields.String()  # TODO Validate it's not already used


class ItemDefinitionSchema(BaseSchema):
    pass


class ItemConditionsSchema(BaseSchema):
    pass


class RoomConditionsSchema(BaseSchema):
    pass


class ItemConditionedUseSchema(BaseSchema):
    pass


class ItemUseSchema(BaseSchema):
    pass


class WorldSchema(BaseSchema):
    version = fields.Integer(required=True, strict=True, validate=validate.OneOf(World.SUPPORTED_VERSIONS))
    name = fields.String(required=True)
    start = fields.String(required=True)  # TODO Validate corresponding room is existing
    description = fields.String()
    author = fields.String()
    items = fields.Dict(keys=fields.Str(), values=fields.Nested(ItemSchema))  # TODO Validate keys can't be "all"
    rooms = fields.Dict(keys=fields.Str(), values=fields.Nested(RoomSchema), required=True, validate=validate.Length(min=1))
