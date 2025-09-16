import os
from typing import Annotated, List

import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

from src.config import settings

router_files = APIRouter()


@router_files.post('/files/upload', tags=['Работа с файлами'], summary='Загрузка одного файла')
async def upload_file(file: Annotated[UploadFile, File(..., description='Загружаемый файл')]):
    async with aiofiles.open(f'{settings.const.base_dir}/{settings.const.dump_path}/upload_{file.filename}', 'wb') as f:
        await f.write(await file.read())


@router_files.post('/files/upload_files', tags=['Работа с файлами'], summary='Множественная загрузка файлов')
async def upload_files(files: Annotated[List[UploadFile], File(..., description='Загружаемый файл')]):
    for file in files:
        async with aiofiles.open(f'{settings.const.base_dir}/{settings.const.dump_path}/1_{file.filename}', 'wb') as f:
            await f.write(await file.read())


@router_files.get('/files/get/{filename}', tags=['Работа с файлами'], summary='Выгрузка с сервера файла целиком')
async def get_file(filename: str):
    if os.path.exists(f'{settings.const.base_dir}/{settings.const.dump_path}/{filename}'):
        return FileResponse(f'{settings.const.base_dir}/{settings.const.dump_path}/{filename}')
    raise HTTPException(404, 'На сервере нет такого файла')


@router_files.get('/files/get/streaming/{filename}', tags=['Работа с файлами'], summary='Выгрузка с сервера файла чанками')
async def get_file_streaming(filename: str):
    if os.path.exists(f'{settings.const.base_dir}/{settings.const.dump_path}/{filename}'):
        return StreamingResponse(generation_chunks(filename), media_type='video/mp4')
    raise HTTPException(404, 'На сервере нет такого файла')


def generation_chunks(filename):
    with open(f'{settings.const.base_dir}/{settings.const.dump_path}/{filename}', 'rb') as file:
        while chunk := file.read(1 * 1024 * 1024): # 1 MB per sec
            yield chunk
