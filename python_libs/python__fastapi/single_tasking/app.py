# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import time
import uvicorn
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

busy = False

def get_result():
    time.sleep(10)
    return "ok"

@app.post("/endpoint")
def endpoint():
    global busy

    if busy:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Resource is busy")

    busy = True
    result = get_result()
    busy = False

    return result

if __name__ == "__main__":
    uvicorn.run(app)
