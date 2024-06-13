from app.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, LargeBinary
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import text
from sqlalchemy.orm import relationship, Session
from app.database import get_db


class Post(Base):
    __tablename__ = "Posts"
    id = Column(Integer, primary_key = True)
    title = Column(String, nullable = False)
    content_text = Column(Text, nullable = False, default = "")
    content_file = Column(LargeBinary)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    # speial sqlalchemy feature that return the relationship of another table
    owner = relationship("User")
    # instead of above pre-built feature, we can actually use joins
        
    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}, published={self.published})>"
    

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key = True)
    username = Column(String, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

    def __repr__(self):
        return f"<User(id = {self.id}, username = {self.username}, email = {self.email})>"

class Profile(Base):
    __tablename__ = "ProfilePhoto"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    photo = Column(LargeBinary)

    def __repr__(self):
        return f"<Profile Photo of User {self.user_id}>"

    

class Vote(Base):
    # composite key(user_id, post_id) -> both set to primary key
    __tablename__ = "Votes"
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("Posts.id", ondelete="CASCADE"), primary_key=True)




