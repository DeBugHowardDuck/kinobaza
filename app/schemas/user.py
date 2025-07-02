from marshmallow import Schema, fields

class UserRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    name = fields.Str()

class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    name = fields.Str()

