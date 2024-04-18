from flask_login import UserMixin
from sqlalchemy import Column,Integer,String,Boolean,Text,ForeignKey
from sqlalchemy.orm import relationship
from flask_proj.db import Base

class User(Base,UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    lastname = Column(String(100),nullable=False)
    password_hash = Column(String(30))
    admin = Column(Boolean)

class Review(Base,UserMixin):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), unique=True, nullable=False)
    text = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"))
    author = Column(String(100),nullable=False)
    comments = relationship('Comments', back_populates='review')

class Comments(Base,UserMixin):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    author = Column(String(100))
    review_id = Column(Integer, ForeignKey('review.id',ondelete="CASCADE"))
    review = relationship('Review', back_populates='comments')