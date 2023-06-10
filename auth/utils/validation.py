from marshmallow import Schema, fields, validate


class CreateRegisterInputSchema(Schema):
    """SignUp fields validation.
    Login must be at least 4 characters, password at least 6 characters.

    """
    username = fields.Str(required=True, validate=validate.Length(min=4, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=50))
    full_name = fields.Str(validate=validate.Length(max=50))



class CreateLoginInputSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4))
    password = fields.Str(required=True, validate=validate.Length(min=6))


class ResetPasswordInputSchema(Schema):
    
    password = fields.Str(required=True, validate=validate.Length(min=6))
    