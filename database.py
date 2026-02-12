from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///employees.db")
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()   # ← MUST come before class

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    department = Column(String)

Base.metadata.create_all(bind=engine)
