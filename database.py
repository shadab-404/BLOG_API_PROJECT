from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = "postgresql://mdshadab:NewPassword123@localhost:5432/shadab"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
