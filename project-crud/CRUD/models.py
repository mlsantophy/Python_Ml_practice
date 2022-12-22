from sqlalchemy import Column,Integer,String
from .database import Base

class User(Base):
    __tablename__='data'
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email= Column(String)
    password=Column(String)
    hm_adrs=Column(String)
    offi_adrs=Column(String)
