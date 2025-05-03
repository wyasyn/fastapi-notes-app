from sqlalchemy.orm import Session
from . import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password: str):
    hashed = pwd_context.hash(password)
    user = models.User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Notes

def get_notes(db: Session, user_id: int):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).all()

def create_note(db: Session, content: str, user_id: int):
    note = models.Note(content=content, owner_id=user_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note_id: int, user_id: int):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == user_id).first()
    if note:
        db.delete(note)
        db.commit()