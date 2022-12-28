import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey, DATE, Boolean, Enum
from .database import Base
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import enum

timeFormat =  datetime.now().strftime('%Y-%m-%d %H:%M')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    created = Column(String, default=timeFormat)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    # profile = relationship("Profile", backref="user")
    # projects
    # profile = relationship("Profile", cascade="all, delete-orphan")
    # reviews
    # skills
    # blogs
    profile = relationship("Profile", back_populates="user")
    # project = relationship("Project", back_populates="owner")



class Profile(Base):
    __tablename__ = 'profiles'

    id  = Column(Integer, primary_key=True,index=True)
    created = Column(String,default=timeFormat)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)
    profile_image = Column(String(500))
    username = Column(String(200), nullable=True)
    location = Column(String(200), nullable=True)
    short_intro = Column(String(200), nullable=True)
    bio = Column(String(2000), nullable=True)
    # profile_image = models.ImageField(
    #     null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")
    social_github = Column(String(200), nullable=True)
    social_twitter = Column(String(200), nullable=True)
    social_linkedin = Column(String(200), nullable=True)
    social_youtube = Column(String(200), nullable=True)
    social_website = Column(String(200), nullable=True)
    is_active = Column(Boolean, nullable=False)
    # is_active = Column(Boolean, nullable=False)
    # owner_id = Column(Integer, ForeignKey("users.id"))
    user_id = Column(Integer,ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")
    # owner_id = Column(Integer, ForeignKey("users.id"),nullable=True)
    project = relationship("Project", back_populates="owner")
    skill = relationship("Skill", back_populates="owner")
    review = relationship("Review", back_populates="owner")
    


class Project(Base):
    
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(String,default=timeFormat)
    title = Column(String(200),nullable=False)
    featured_image = Column(String(500))
    description = Column(String(2000), nullable=False)
    demo_link = Column(String(2000),nullable = True)
    source_link = Column(String(2000), nullable=True)
    vote_total = Column(Integer,default=0)
    vote_ratio = Column(Integer,default=0)
    # ForeignKeys
    owner_id = Column(Integer,ForeignKey("profiles.id"))
    owner = relationship("Profile", back_populates="project")
    review = relationship("Review", back_populates="project")
    # Relationships
    # owner
    # tags

    
class Review(Base):
    
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(String,default=timeFormat)
    comment = Column(String(200),nullable=False)
    vote_value = Column(String,nullable=False)
    # Relationships
    owner_id = Column(Integer,ForeignKey("profiles.id"))
    owner = relationship("Profile", back_populates="review")

    project_id = Column(Integer,ForeignKey("projects.id"))
    project = relationship("Project", back_populates="review")
   


class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, index=True)
    created = Column(String, default=timeFormat) 
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    owner_id = Column(Integer,ForeignKey("profiles.id"))
    owner = relationship("Profile", back_populates="skill")
    # owner

