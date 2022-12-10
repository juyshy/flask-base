from flask_marshmallow import Schema

class PhotoSchema(Schema):
    class Meta:
        fields = (
            'id', 'user_id', 'pagenum', 'pageOne', 'aml', 'name', 'filePath', 'casetteNums', 'notes', 'taken',
            'created_at',
            'updated_at', 'rotation')