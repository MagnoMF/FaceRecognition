from db.init_db import SessionLocal
from models.user import User
from datetime import datetime

def create(ds_name, cd_role, session=SessionLocal):
    with session() as session:
        new_user = User(ds_name=ds_name, cd_role=cd_role)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user
