# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import time
from typing import Annotated, Dict, Any
import uvicorn
from fastapi import (
    FastAPI,
    HTTPException,
    BackgroundTasks,
    Depends,
    Path,
    Query,
    Header
)

def simple_task(msg: str):

    print("simple_task", 1, msg)
    time.sleep(2)
    print("simple_task", 2, msg)
    time.sleep(2)
    print("simple_task", 3, msg)
    time.sleep(2)
    print("simple_task", 4, msg)

def backfround_task(msg: str):

    print("backfround_task", 1, msg)
    time.sleep(1)
    print("backfround_task", 2, msg)
    time.sleep(1)
    print("backfround_task", 3, msg)
    time.sleep(1)
    print("backfround_task", 4, msg)


class MyDependency:
    def __init__(self, my_path: str):
        self.msg = my_path


async def my_dependency(
    my_path: Annotated[str, Path(description="path")],
    my_query: Annotated[str, Query(description="query")],
    my_header: Annotated[str, Header(description="header")]
) -> Dict[str, Any]:

    return {
        "my_path": my_path,
        "my_query": my_query,
        "my_header": my_header
    }


app = FastAPI()

@app.post("/api/{my_path}")
async def print_num(
    my_path: str,
    backfround_tasks: BackgroundTasks,
    dependency_function: Annotated[Dict[str, Any], Depends(my_dependency)],
    dependency_class: MyDependency = Depends(MyDependency)):

    if my_path not in ['msg1', 'msg2']:
        raise HTTPException(400)

    print("dependency_class.msg:", dependency_class.msg)
    print("dependency_function:", dependency_function)

    backfround_tasks.add_task(backfround_task, my_path)

    simple_task(my_path)

    return "ok"

if __name__ == "__main__":

    uvicorn.run(app)
