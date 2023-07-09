from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from database import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def getRoutes():
    return ['/notes', '/notes/{ID}']  # Use curly braces for path parameters

@app.get("/notes")
def getNotes():
    notes = db.sql('SELECT * FROM notesapp.notes ORDER BY __updatedtime__ DESC')
    return notes

@app.get("/notes/{id}")
def getNote(id: str):
    notes = db.search_by_hash('notesapp', 'notes', [id], get_attributes=['*'])
    return notes[0]

@app.post("/notes")
def addNotes(data: dict = Body(...)):
    note = {
        "candidate": data.get('candidate'),
        "name": data.get('name'),
        "age": data.get('age'),
        "joinDate": data.get('joinDate'),
        "rate": data.get('rate')
    }
    db.insert('notesapp', 'notes', [note])
    notes = db.sql('SELECT * FROM notesapp.notes')
    return notes

@app.put("/notes/{id}")
def updateNote(id: str, data: dict = Body(...)):
    note = db.update('notesapp', 'notes', [{"id": id, "body": data.get("body")}])
    notes = db.sql('SELECT * FROM notesapp.notes')
    return notes

@app.delete("/notes/{id}")
def deleteNote(id: str):
    db.delete('notesapp', 'notes', [id])
    notes = db.sql('SELECT * FROM notesapp.notes')
    return notes
