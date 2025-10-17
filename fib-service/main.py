from fastapi import FastAPI, HTTPException
from functools import lru_cache
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

app = FastAPI(title="fibonacci-service")

# DB setup
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://algo_user:algo_pass@db:5432/algo_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class FibonacciResult(Base):
    __tablename__ = "fibonacci_results"
    id = Column(Integer, primary_key=True)
    n = Column(Integer, unique=True)
    result = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# In-memory caching
@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.get("/fibonacci/{n}")
async def fibonacci(n: int):
    db = SessionLocal()
    try:
        # Check DB first
        record = db.query(FibonacciResult).filter(FibonacciResult.n == n).first()
        if record:
            return {"n": n, "fibonacci": record.result, "cached": True}

        # Compute result and save
        result = fib(n)
        db.add(FibonacciResult(n=n, result=result))
        db.commit()
        return {"n": n, "fibonacci": result, "cached": False}
    finally:
        db.close()
