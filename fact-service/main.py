from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from math import factorial as math_factorial

app = FastAPI(title="factorial-service")

# DB setup
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://algo_user:algo_pass@db:5432/algo_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class FactorialResult(Base):
    __tablename__ = "factorial_results"
    id = Column(Integer, primary_key=True)
    n = Column(Integer, unique=True)
    result = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

@app.get("/factorial/{n}")
async def factorial(n: int):
    db = SessionLocal()
    try:
        record = db.query(FactorialResult).filter(FactorialResult.n == n).first()
        if record:
            return {"n": n, "factorial": record.result, "cached": True}

        if n < 0:
            raise HTTPException(status_code=400, detail="n must be >= 0")

        result = math_factorial(n)
        db.add(FactorialResult(n=n, result=result))
        db.commit()
        return {"n": n, "factorial": result, "cached": False}
    finally:
        db.close()
