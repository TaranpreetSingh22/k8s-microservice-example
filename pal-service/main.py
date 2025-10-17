from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

app = FastAPI(title="palindrome-service")

# ✅ Database setup
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://algo_user:algo_pass@db:5432/algo_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ✅ Database model
class PalindromeResult(Base):
    __tablename__ = "palindrome_results"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    is_palindrome = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

# ✅ Create table if not exists
Base.metadata.create_all(bind=engine)

# ✅ Helper function
def check_palindrome(text: str) -> bool:
    s = ''.join(ch.lower() for ch in text if ch.isalnum())
    return s == s[::-1]

# ✅ API route
@app.get("/is_palindrome/{text}")
async def is_palindrome(text: str):
    db = SessionLocal()
    try:
        # Check if result already exists
        record = db.query(PalindromeResult).filter(PalindromeResult.text == text).first()
        if record:
            return {"text": text, "is_palindrome": record.is_palindrome, "cached": True}

        # Compute and store
        result = check_palindrome(text)
        db.add(PalindromeResult(text=text, is_palindrome=result))
        db.commit()

        return {"text": text, "is_palindrome": result, "cached": False}
    finally:
        db.close()
