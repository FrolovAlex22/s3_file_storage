import os
from fastapi import APIRouter, Response
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from core.config import s3_client


router_s3 = APIRouter(
    prefix="/file_storage",
    tags=["s3_storage"],
)


@router_s3.get("/")
def index():
    return {"status": "fastapi file storage service is running."}


@router_s3.post("/upload_file")
async def upload_file_to_s3():
    await s3_client.upload_file("name")
    print("file saved to s3")


@router_s3.get("/get_file")
async def get_file_to_s3(bg_tasks: BackgroundTasks):
    await s3_client.get_file("test.jpg", "data/test_local_file.jpg")
    file = "data/test_local_file.jpg"
    if not file:
        raise Exception("file not found")
    bg_tasks.add_task(os.remove, file)
    return FileResponse(
        file,
        background=bg_tasks
        )


@router_s3.post("/delete_file")
async def delete_file_to_s3():
    await s3_client.delete_file("test.jpg")
    return Response(
        status_code=200,
        content="file has been deleted from s3 storage"
    )
