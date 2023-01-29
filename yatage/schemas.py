from marshmallow import Schema, fields, validate, validates_schema, ValidationError, EXCLUDE
from yatage.world import World


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class RoomSchema(BaseSchema):
    items = fields.List(fields.String())  # TODO Validate items are existing
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
    use = fields.Method(deserialize='deserialize_use')

    def deserialize_use(self, value):
        if isinstance(value, str):
            return fields.String()
        elif isinstance(value, dict):
            if 'text' in value:
                return fields.Nested(ItemUseSchema)
            elif 'items_conditions' in value or 'room_conditions' in value:
                return fields.Nested(ItemConditionedUseSchema)


class ItemDefinitionSchema(BaseSchema):
    pass


class ItemConditionsSchema(BaseSchema):
    pass


class RoomConditionsSchema(BaseSchema):
    pass


class ItemConditionedUseSchema(BaseSchema):
    pass


class ItemUseSchema(BaseSchema):
    text = fields.String(required=True)
    remove = fields.List(fields.String())  # TODO Validate items are existing
    spawn = fields.List(fields.String())  # TODO Validate items are existing
    mark_used = fields.List(fields.String())  # TODO Validate items are existing
    teleport = fields.String()  # TODO Validate room is existing


class WorldSchema(BaseSchema):
    version = fields.Integer(required=True, strict=True, validate=validate.OneOf(World.SUPPORTED_VERSIONS))
    name = fields.String(required=True)
    start = fields.String(required=True)
    description = fields.String()
    author = fields.String()
    items = fields.Dict(keys=fields.String(validate=validate.NoneOf(('all',))), values=fields.Nested(ItemSchema))
    rooms = fields.Dict(keys=fields.String(), values=fields.Nested(RoomSchema), required=True, validate=validate.Length(min=1))

    @validates_schema
    def validate_schema(self, data: dict, **kwargs):
        errors = {}

        if data.get('start') not in data.get('rooms', {}):
            errors['start'] = [
                'Room not found',
            ]

        if errors:
            raise ValidationError(errors)
