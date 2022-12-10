from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean

from .. import db

class Book(db.Model):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    book_type = Column(String)
    language = Column(String)
    name = Column(String)

