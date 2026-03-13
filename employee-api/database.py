import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./employees.db")

engine = create_engine(
    DATABASE_URL,connect_args={"check_same_thread":False}
    )
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()   # ← MUST come before class

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    department = Column(String)
