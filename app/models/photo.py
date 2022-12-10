from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean

from .. import db

class Photo(db.Model):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    pagenum = Column(Integer)
    pageOne = Column(Integer)
    aml = Column(Integer)
    name = Column(String(50))
    filePath = Column(String(250))
    casetteNums = Column(String(100))
    notes = Column(String(500))
    taken = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    rotation = Column(Integer)
