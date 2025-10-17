from fastapi import FastAPI

app = FastAPI(title="palindrome-service")

@app.get("/is_palindrome/{text}")
async def is_palindrome(text: str):
    s = ''.join(ch.lower() for ch in text if ch.isalnum())
    return {"text": text, "is_palindrome": s == s[::-1]}
