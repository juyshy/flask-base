from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean

from .. import db

class Photo(db.Model):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    pagenum = Column(Integer)
    pageOne = Column(Integer)
    aml = Column(Integer)
    name = Column(String)
    filePath = Column(String)
    casetteNums = Column(String)
    notes = Column(String)
    taken = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    rotation = Column(Integer)
