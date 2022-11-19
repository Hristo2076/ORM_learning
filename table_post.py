from sqlalchemy import TIMESTAMP,Float,ForeignKey, Column,Integer,String,DateTime
from database import Base,engine,SessionLocal

class Post(Base):
    __tablename__="post"
    __table_args__={"schema":"public"}

    id = Column(Integer,primary_key=True)
    text = Column(String)
    topic = Column(String)


if __name__=='__main__':
    session = SessionLocal()
    g = []
    result = session\
        .query(Post.id,Post.text,Post.topic)\
        .filter(Post.topic == 'business')\
        .order_by(Post.id.desc())\
        .limit(10)\
        .all()
    for i in result:
        g.append(i[0])
    print(g)


