from fastapi import FastAPI
import math

app = FastAPI(title="prime-service")

@app.get("/is_prime/{n}")
async def is_prime(n: int):
    if n < 2:
        return {"n": n, "is_prime": False}
    if n in (2, 3):
        return {"n": n, "is_prime": True}
    if n % 2 == 0:
        return {"n": n, "is_prime": False}
    r = int(math.sqrt(n))
    for i in range(3, r+1, 2):
        if n % i == 0:
            return {"n": n, "is_prime": False}
    return {"n": n, "is_prime": True}
