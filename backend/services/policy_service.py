from sqlalchemy.orm import Session
from models.policy import Policy

def get_policy(db:Session):
    return db.query(Policy).first()