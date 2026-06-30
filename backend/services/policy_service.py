from sqlalchemy.orm import Session
from models.policy import Policy

def get_policy(db:Session,business_id):
    return db.query(Policy).filter(
        Policy.business_id == business_id
    ).first()