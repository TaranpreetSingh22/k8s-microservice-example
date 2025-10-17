from fastapi import FastAPI, HTTPException
from functools import lru_cache

app = FastAPI(title="fibonacci-service")

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
    try:
        return {"n": n, "fibonacci": fib(n)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
