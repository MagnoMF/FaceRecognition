from db.init_db import SessionLocal
from models.user import User

def create(ds_name, city, session=SessionLocal):
    with session() as session:
        new_user = User(ds_name=ds_name, city=city)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user
