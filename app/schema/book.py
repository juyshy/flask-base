from flask_marshmallow import Schema

class BookSchema(Schema):
    class Meta:
        fields = ('book_id', 'book_type', 'language', 'name')
