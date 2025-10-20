from sqlalchemy import column, Integer,String, DateTime,Enum,Email


from db import Base
class user(Base):
    __tablename__ = "users"
    id= column(Integer, primary_key=True)
    email= column(String,unique=True,nullable=False)