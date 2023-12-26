from sqlalchemy.orm import Session
import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.Userd).filter(models.Userd.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Userd).filter(models.Userd.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Userd).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.Userd(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Itemd).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Itemd(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item