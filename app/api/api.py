from fastapi import FastAPI
from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_tz_aware(date_time):
    if date_time.tzinfo is not None and date_time.tzinfo.utcoffset(date_time) is not None:
        return True
    else:
        return False
