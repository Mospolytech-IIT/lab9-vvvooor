from sqlalchemy.orm import Session
from app import models, schemas

# Получить всех пользователей
def get_users(db: Session):
    return db.query(models.User).all()

# Создать нового пользователя
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Получить все посты
def get_posts(db: Session):
    return db.query(models.Post).all()

# Создать новый пост
def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
