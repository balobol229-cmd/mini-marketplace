from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from models import NoteDB
from schemas import NoteCreate, NotePublic
from security import get_current_user


router = APIRouter(prefix="/notes", tags=["notes"])



@router.post("")
def Note_Create(note_data: NoteCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if not note_data.text.strip():
        raise HTTPException(status_code = 400, detail = "заметка не должна быть пустой")
    

    new_note = NoteDB(text = note_data.text, user_id = current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {"id": new_note.id, "text": note_data.text, "user_id": new_note.user_id}

@router.get("")
def Show_Notes(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    notes_public_list = []

    notes = db.query(NoteDB).filter(NoteDB.user_id == current_user.id).all()
    for note in notes:
        notes_public = NotePublic(text = note.text, id = note.id)

        notes_public_list.append(notes_public)
    return notes_public_list

@router.delete("/{note_id}")
def Delete_Note(note_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if note is None:
        raise HTTPException(status_code = 404, detail = "не найдено")
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail = "не найдено юзера такого нах")

    db.delete(note)
    db.commit()
    return {"ok": "True"}




@router.patch("/{note_id}")
def update_note(note_id: int, note_text: str, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if not note_text.strip():
        raise HTTPException(status_code = 400, detail = "нельзя обновить на воздух")
    
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if note is None:
        raise HTTPException(status_code = 404, detail = "Такой заметки нет")
    if note.user_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "Не твоя заметка")
    note.text = note_text

    db.commit()
    db.refresh(note)
 
    return {"id": note.id, "text": note.text}


@router.get("/{note_id}")
def OpenNotes(note_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    notes = db.query(NoteDB).filter(NoteDB.id == note_id).first()

    if not notes:
        raise HTTPException(status_code = 404, detail = "Такой задачи не найдено/Такой задачи нет")
    
    if notes.user_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "Такой задачи нет в вашем профиле") 

    return {"id": notes.id, "text": notes.text}


