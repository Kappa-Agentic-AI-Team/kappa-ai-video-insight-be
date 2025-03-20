import os
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine,URL, Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError

#Database setup
#DATABASE_URL=URL.create("sqlite",host="localhost",database="chat_history.db")
DATABASE_URL="sqlite:///searchHistory.db"
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})
SessionLocal=sessionmaker(bind=engine, autoflush=False,autocommit=False)

#SQLAlchemy ORM model
Base= declarative_base()


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username= Column(String,unique=True, index=True)
    name= Column(String)
    image=Column(String)
    hashed_password= Column(String)
    

class SearchHistory(Base):
    __tablename__ = "search_history" 
    
    id = Column(Integer,primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    query= Column(Text)
    summary = Column(Text)
    
    
    user= relationship("User")

#Create Tables
Base.metadata.create_all(bind=engine)

#OAuth2 for authentication
oauth2_scheme =OAuth2PasswordBearer(tokenUrl="Login")

#pydantic models
class CreateUser(BaseModel):
    username: str
    password: str
    name: str
    image: str| None

class SearchText(BaseModel):
    password: str
    username: str
    text: str
    
class Search(BaseModel):
    text:str 