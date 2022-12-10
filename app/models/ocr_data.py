
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean,Text

from .. import db

class OcrData(db.Model):
    __tablename__ = 'ocr_data'
    id = Column(Integer, primary_key=True)
    photo_id = Column(Integer, db.ForeignKey('photos.id'))
    photo = db.relationship("Photo", backref=db.backref("photos", uselist=False))
    ocr = Column(Text)
    hocr = Column(Text(300000))
    hocr_edited = Column(Text(300000))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    saved_selection = Column(Text)
    user_id = Column(Integer)

