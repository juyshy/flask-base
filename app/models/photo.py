from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean

from .. import db

class Photo(db.Model):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    filePath = Column(String(255))
    taken = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    casetteNums = Column(String(20))
    notes = Column(String(100))
    user_id = Column(Integer)
    pagenum = Column(Integer)
    pageOne = Column(Integer)
    aml = Column(Integer)
    rotation = Column(Integer)
