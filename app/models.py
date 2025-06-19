from typing import Optional
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin
from app import login
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5

Base = declarative_base()



@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
class User(Base):
    __tablename__ = 'user'

    id: so.Mapped[str] = so.mapped_column(Integer, primary_key=True, autoincrement=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Post(Base):
    __tablename__ = 'post'
    id: so.Mapped[int] = so.mapped_column(Integer,primary_key = True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id : so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User]= so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
