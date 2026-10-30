from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import NoteDB, UserDB
from schemas import NoteCreate, NotePublic
from security import get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])


def _get_own_note(note_id: int, user: UserDB, db: Session) -> NoteDB:
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    if note.user_id != user.id:
        raise HTTPException(status_code=403, detail="Это не ваша заметка")
    return note


@router.post("", response_model=NotePublic)
def create_note(
    note_data: NoteCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not note_data.text.strip():
        raise HTTPException(status_code=400, detail="Заметка не должна быть пустой")

    note = NoteDB(text=note_data.text, user_id=current_user.id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("", response_model=list[NotePublic])
def list_notes(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(NoteDB).filter(NoteDB.user_id == current_user.id).all()


@router.get("/{note_id}", response_model=NotePublic)
def get_note(
    note_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _get_own_note(note_id, current_user, db)


@router.patch("/{note_id}", response_model=NotePublic)
def update_note(
    note_id: int,
    note_text: str,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not note_text.strip():
        raise HTTPException(status_code=400, detail="Текст заметки не должен быть пустым")

    note = _get_own_note(note_id, current_user, db)
    note.text = note_text
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = _get_own_note(note_id, current_user, db)
    db.delete(note)
    db.commit()
    return {"ok": True}
