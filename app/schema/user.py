from flask_marshmallow import Schema

class UserSchema(Schema):
    class Meta:
        fields = ( 'id', 'first_name', 'last_name', 'email', 'created_at', 'role_id' )