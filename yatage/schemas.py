from marshmallow import Schema, fields, validate, validates_schema, ValidationError, EXCLUDE
from yatage.world import World


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class RoomSchema(BaseSchema):
    items = fields.List(fields.Str())  # TODO Validate items are existing
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
    start = fields.String(required=True)
    description = fields.String()
    author = fields.String()
    items = fields.Dict(keys=fields.Str(validate=validate.NoneOf(('all',))), values=fields.Nested(ItemSchema))
    rooms = fields.Dict(keys=fields.Str(), values=fields.Nested(RoomSchema), required=True, validate=validate.Length(min=1))

    @validates_schema
    def validate_schema(self, data: dict, **kwargs):
        errors = {}

        if data.get('start') not in data.get('rooms', {}):
            errors['start'] = [
                'Room not found'
            ]

        if errors:
            raise ValidationError(errors)
