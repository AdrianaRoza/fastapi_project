from models import db
from sqlalchemy.orm import sessionmaker

def capture_session():
    Session = sessionmaker(bind=db)
    session = Session()

    return session