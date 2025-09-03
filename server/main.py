from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/query/")
async def query(
        file: Annotated[bytes, File()],
        query: Annotated[str, Form()]
    ):
    print(file, type(file))
    print(query)
    return {"file_size": len(file)}