from db.init_db import SessionLocal
from models.pictures import Pictures
from services.face_recognition import FaceRecognition
from sqlalchemy import text

def create(cd_user, img_upload, session=SessionLocal):
    face = FaceRecognition(img_upload)
    ebedding = face.to_embeddings()
    with session() as session:
        new_picture = Pictures(cd_user=cd_user, picture_vector=ebedding.tolist())
        session.add(new_picture)
        session.commit()

def find_image(img_upload, session=SessionLocal):
    face = FaceRecognition(img_upload)
    ebedding = face.to_embeddings()
    threshold = 0.5
    string_representation = "[" + ",".join(str(x) for x in ebedding.tolist()) + "]"
    query = f"SELECT * FROM pictures WHERE picture_vector <-> :string_representation < :threshold ORDER BY picture_vector <-> :string_representation LIMIT 1;"
    with session() as session:
        picture = session.execute(text(query), {"string_representation": string_representation, "threshold": threshold}).all()
        distance = session.execute(text(f"SELECT picture_vector <-> '{string_representation}' FROM pictures ORDER BY picture_vector <-> '{string_representation}' LIMIT 1;")).all()
        print("distance", distance)
    if(not picture):
        return "Não foi encontrado rostos cadastrados"
    return picture[0].cd_user