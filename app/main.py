from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import models, database, crud
from .auth import authenticate_user, create_access_token, get_current_user, get_db

# Pydantic schemas
class UserCreate(BaseModel):
    username: str
    password: str

class NoteCreate(BaseModel):
    content: str

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = crud.create_user(db, user.username, user.password)
    return {"username": new_user.username, "id": new_user.id}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.get("/notes")
def read_notes(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_notes(db, current_user.id)

@app.post("/notes")
def add_note(note: NoteCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_note(db, note.content, current_user.id)

@app.delete("/notes/{note_id}")
def remove_note(note_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_note(db, note_id, current_user.id)
    return {"message": "Note deleted"}
