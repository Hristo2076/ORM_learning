from sqlalchemy import TIMESTAMP,Float,ForeignKey, Column,Integer,String,DateTime
from database import Base,engine,SessionLocal
from sqlalchemy import desc, func

class User(Base):
    __tablename__="user"
    __table_args__ = {"schema": "public"}
    id = Column(Integer,primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)

if __name__=="__main__":
    session = SessionLocal()
    g = []
    for group in (session\
        .query(User.country,User.os,func.count(User.id).label('count'))\
        .filter(User.exp_group == 3)\
        .group_by(User.country,User.os)\
        .having(func.count(User.id)>100)\
        .order_by(desc(func.count("*")))\
        .all()
    ):
        g.append((group.country,group.os,group.count))
    print(g)