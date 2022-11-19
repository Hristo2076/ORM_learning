from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from sqlalchemy import func,desc

from database import SessionLocal
from table_feed import User, Post, Feed
from schema import UserGet, PostGet, FeedGet

app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db

@app.get("/user/{id}",response_model=UserGet)
def get_users(id, limit: int=10, db: Session=Depends(get_db)):
    result = db.query(User)\
        .filter(User.id==id)\
        .limit(limit)\
        .one_or_none()
    if not result:
        raise HTTPException(404,"ERROR")
    else:
        return result

@app.get("/post/{id}",response_model=PostGet)
def get_post(id,limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Post)\
        .filter(Post.id==id)\
        .limit(limit)\
        .one_or_none()
    if not result:
        raise HTTPException(404,"ERROR")
    else:
        return result

@app.get("/user/{id}/feed",response_model=List[FeedGet])
def get_users(id, limit: int=10, db: Session=Depends(get_db)):
    result = db.query(Feed)\
        .filter(Feed.user_id==id)\
        .order_by(Feed.time.desc())\
        .limit(limit)\
        .all()
    if not result:
        raise HTTPException(200)
    else:
        return result

@app.get("/post/{id}/feed",response_model=List[FeedGet])
def get_post(id,limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed)\
        .filter(Feed.post_id==id)\
        .order_by(Feed.time.desc())\
        .limit(limit)\
        .all()
    if not result:
        raise HTTPException(200)
    else:
        return result



@app.get("/post/recommendations/")
def get_recommendation(id =1,limit: int = 10,db: Session = Depends(get_db)):
    result = db.query(Post)\
        .select_from(Feed)\
        .filter(Feed.action == 'like')\
        .join(Post)\
        .group_by(Post.id)\
        .order_by(func.count(Post.id).desc())\
        .limit(limit)\
        .all()
    return result