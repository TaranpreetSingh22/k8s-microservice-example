from fastapi import FastAPI, HTTPException
import math

app = FastAPI(title="factorial-service")

@app.get("/factorial/{n}")
async def factorial(n: int):
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be >= 0")
    if n > 1000:
        raise HTTPException(status_code=400, detail="n too large")
    return {"n": n, "factorial": math.prod(range(1, n+1)) if n>0 else 1}
