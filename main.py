from fastapi import FastAPI, Body, File, UploadFile, HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import db
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

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
    if notes:
        return notes[0]
    else:
        raise HTTPException(status_code=404, detail="Note not found")

@app.post("/notes")
def addNotes(data: dict = Body(...)):
    note = {
        "candidate": data.get('candidate'),
        "name": data.get('name'),
        "age": data.get('age'),
        "joinDate": data.get('joinDate'),
        "rate": data.get('rate'),
        "dRate": data.get('dRate')
    }
    db.insert('notesapp', 'notes', [note])
    notes = db.sql('SELECT * FROM notesapp.notes')
    return notes

# @app.put("/note/{id}")
# def updateNote(id: str, data: dict = Body(...)):
#     # note = db.update('notesapp', 'notes', [{"id": id, "body": data.get("body")}])
#     db.update('notesapp', 'notes', [{"id":id, "rate":data["rate"]}])
#     notes = db.sql('SELECT * FROM notesapp.notes')
#     return notes

# @app.put("/notes/{id}")
# def updateNote(id: str, data: dict = Body(...)):
#     note = {
#         "id": id,
#         "candidate": data.get('candidate'),
#         "name": data.get('name'),
#         "age": data.get('age'),
#         "joinDate": data.get('joinDate'),
#         "rate": data.get('rate'),
#         "dRate": data.get('dRate')
#     }
#     db.update('notesapp', 'notes', [note])
#     notes = db.sql('SELECT * FROM notesapp.notes')
#     return notes
@app.put("/notes/{id}")
def updateNote(id: str, data: dict = Body(...)):
    global overall_defect_percentage
    overall_defect_percentage = 0.0  # Reset the overall_defect_percentage value to zero

    note = {
        "id": id,
        "candidate": data.get('candidate'),
        "name": data.get('name'),
        "age": data.get('age'),
        "joinDate": data.get('joinDate'),
        "rate": data.get('rate'),
        "dRate": data.get('dRate')
    }
    db.update('notesapp', 'notes', [note])
    notes = db.sql('SELECT * FROM notesapp.notes')
    return notes

#search
@app.get("/search", response_model=List[dict])
def search_notes(
    candidate: str = Query(None),
    name: str = Query(None),
    age: int = Query(None),
    joinDate: str = Query(None),
    rate: float = Query(None),
    dRate: float = Query(None)
):
    notes = db.sql('SELECT * FROM notesapp.notes')  # Fetch all notes from the database
    results = []

    for note in notes:
        # Check if the note matches the search criteria
        if (
            (candidate is None or note["candidate"] == candidate) and
            (name is None or note["name"] == name) and
            (age is None or note["age"] == age) and
            (joinDate is None or note["joinDate"] == joinDate) and
            (rate is None or note["rate"] == rate) and
            (dRate is None or note["dRate"] == dRate)
        ):
            results.append(note)

    return results


@app.delete("/notes/{id}")
def deleteNote(id: str):
    db.delete('notesapp', 'notes', [id])
    notes = db.sql('SELECT * FROM notesapp.notes')
    return notes

MODEL = tf.keras.models.load_model('./model/garment.h5')
CLASS_NAMES = ["defect3", "non-defect", "open-defect", "wavy-seam-defect"]

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    try:
        image = Image.open(BytesIO(data))
        # Resize image to (256, 256)
        image = image.resize((256, 256))
        image = np.array(image)
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file")

prediction_counter = 0
defect_counter = 0
overall_defect_percentage = 0.0

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global prediction_counter, defect_counter, overall_defect_percentage

    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]

    prediction_counter += 1

    if predicted_class in ["defect3", "open-defect", "wavy-seam-defect"]:
        defect_counter += 1

    confidence = np.max(predictions[0])
    response = {
        'class': predicted_class,
        'confidence': float(confidence)
    }

    if prediction_counter % 5 == 0:
        overall_defect_percentage = (defect_counter / prediction_counter) * 100.0

    if prediction_counter == 5:
        prediction_counter = 0
        defect_counter = 0

    response['overall_defect_percentage'] = overall_defect_percentage

    return response


MODEL2 = tf.keras.models.load_model('./model/garmentplots4.h5')
CLASS_NAMES2 = ["CoP+IoP+Washer+Bolt", "CoP+IoP+Washer+Bolt+No Bolt", "CoP+Washers+Bolt+No Bolt", "CoP+Washers+No Washer",  "Correct Orientation+Washers", "Correct Orientation+Washers+Bolts", "Correct Orientation of Pegs", "Incorrect Orientation of Pegs", "Incorrect Orientation+Washers", "Incorrect Orientation+Washers+Bolts", "IoP+CoP pegs", "IoP+CoP+Washer+No Washer", "IoP+CoP+Washers", "IoP+Washers+Bolt+No Bolt", "No Pegs", "IoP+Washers+No Washer", "IoP+CoP+Washer+Bolt+No Bolt"]

@app.post("/predict2")
async def predict2(file: UploadFile = File(...)):
    global prediction_counter, defect_counter, overall_defect_percentage

    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL2.predict(img_batch)
    predicted_class = CLASS_NAMES2[np.argmax(predictions[0])]

    prediction_counter += 1

    if predicted_class in["CoP+IoP+Washer+Bolt", "CoP+IoP+Washer+Bolt+No Bolt", "CoP+Washers+Bolt+No Bolt", "CoP+Washers+No Washer",  "Correct Orientation+Washers", "Correct Orientation+Washers+Bolts", "Correct Orientation of Pegs", "Incorrect Orientation of Pegs", "Incorrect Orientation+Washers", "Incorrect Orientation+Washers+Bolts", "IoP+CoP pegs", "IoP+CoP+Washer+No Washer", "IoP+CoP+Washers", "IoP+Washers+Bolt+No Bolt", "IoP+Washers+No Washer", "IoP+CoP+Washer+Bolt+No Bolt"]:
        defect_counter += 1

    confidence = np.max(predictions[0])
    response = {
        'class': predicted_class,
        'confidence': float(confidence)
    }

    if prediction_counter % 5 == 0:
        overall_defect_percentage = (defect_counter / prediction_counter) * 100.0

    if prediction_counter == 5:
        prediction_counter = 0
        defect_counter = 0

    response['overall_defect_percentage'] = overall_defect_percentage

    return response
