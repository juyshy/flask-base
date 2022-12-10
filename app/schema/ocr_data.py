from flask_marshmallow import Schema

class OcrDataSchema(Schema):
    class Meta:
        fields = ( 'id', 'photo_id', 'ocr', 'hocr', 'hocr_edited', 'created_at', 'updated_at', 'saved_selection', 'user_id')