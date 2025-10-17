from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import math
import os

app = FastAPI(title="prime-service")

# ✅ Database setup
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://algo_user:algo_pass@db:5432/algo_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ✅ Database model
class PrimeResult(Base):
    __tablename__ = "prime_results"
    id = Column(Integer, primary_key=True, index=True)
    n = Column(Integer, unique=True, index=True)
    is_prime = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

# ✅ Create table
Base.metadata.create_all(bind=engine)

# ✅ Prime checker
def check_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    r = int(math.sqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

# ✅ API route
@app.get("/is_prime/{n}")
async def is_prime(n: int):
    db = SessionLocal()
    try:
        # Check if already stored
        record = db.query(PrimeResult).filter(PrimeResult.n == n).first()
        if record:
            return {"n": n, "is_prime": record.is_prime, "cached": True}

        # Compute and store
        result = check_prime(n)
        db.add(PrimeResult(n=n, is_prime=result))
        db.commit()

        return {"n": n, "is_prime": result, "cached": False}
    finally:
        db.close()
