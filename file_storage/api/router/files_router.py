import os

import aiofiles
from fastapi import APIRouter, BackgroundTasks, Depends, Request, UploadFile
from fastapi.responses import FileResponse

from api.router.auth_router import get_current_user
from db.db import (
    add_file, get_all_user_file, find_file_by_name, find_and_delete_file
)
from core.models.user_model import Users
from core.config import s3_client
from crud.s3_client import encoding_s3_name, decoding_s3_name

router_files = APIRouter()


@router_files.get("/")
async def get_files(
    current_user: Users = Depends(get_current_user)
):
    files = await get_all_user_file(current_user)
    return files


@router_files.get("/download")
async def download_file(
    file_name: str,
    bg_tasks: BackgroundTasks,
    current_user: Users = Depends(get_current_user)

):
    encoding_name = await encoding_s3_name(current_user.id, file_name)
    check_file = await find_file_by_name(current_user.id, file_name)
    if not check_file:
        return {"message": "file not found"}
    full_path = os.path.join("data", encoding_name)
    try:
        # Получение временного файла
        file = await s3_client.get_file(encoding_name, full_path)
        media_type = file.name.split(".")[-1]
        # Удаление временного файла
        bg_tasks.add_task(os.remove, full_path)
        return FileResponse(
            path=full_path, filename=file_name, media_type=media_type, background=bg_tasks
        )
    except Exception as e:
        return {"message": e.args}


@router_files.post("/upload")
async def upload_file(
    file: UploadFile,
    current_user: Users = Depends(get_current_user),
):
    full_path = os.path.join("data", file.filename)
    if await find_file_by_name(current_user.id, file.filename):
        return {"message": "File already exists"}
    file_name = await encoding_s3_name(current_user.id, file.filename)
    try:
        async with aiofiles.open(full_path, "wb") as out_file:
            content = await file.read()
            file_size = len(content)
            await out_file.write(content)
            await s3_client.upload_file(file_path=full_path, name=file_name)
            await add_file(file.filename, file_size, current_user)
            return {"message": "File saved successfully"}
    except Exception as e:
        return {"message": e.args}
    finally:
        os.remove(full_path)


@router_files.post("/delete")
async def delete_file(
    name: str,
    current_user: Users = Depends(get_current_user)
):
    print(name)
    if not await find_file_by_name(current_user.id, name):
        return {"message": "The file is not in the list of added files"}
    s3_file_name = await encoding_s3_name(current_user.id, name)
    try:
        await s3_client.delete_file(s3_file_name)
        await find_and_delete_file(current_user.id, name)
        return {"message": "File deleted successfully"}
    except Exception as e:
        return {"message": e.args}
