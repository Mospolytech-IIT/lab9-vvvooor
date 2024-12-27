from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, crud
from app.database import engine, SessionLocal

# Создание таблиц, если они ещё не существуют
models.Base.metadata.create_all(bind=engine)

# Инициализация приложения FastAPI
app = FastAPI()

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Получить всех пользователей
@app.get("/users", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

# Создать нового пользователя
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверка на уникальность username и email
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username or email already exists"
        )
    return crud.create_user(db, user)

# Получить все посты
@app.get("/posts", response_model=List[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return posts

# Создать новый пост
@app.post("/posts", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Проверка существования пользователя
    user = db.query(models.User).filter(models.User.id == post.user_id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="User with the given ID does not exist"
        )
    return crud.create_post(db, post)

# Удалить пост по ID
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted successfully"}

# Удалить пользователя и все его посты
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Удаление связанных постов
    db.query(models.Post).filter(models.Post.user_id == user.id).delete()
    # Удаление пользователя
    db.delete(user)
    db.commit()
    return {"detail": "User and all their posts deleted successfully"}

