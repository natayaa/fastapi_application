from fastapi import APIRouter, status, UploadFile, File, HTTPException
from fastapi import Request, Depends
from fastapi.responses import JSONResponse

from PIL import Image

import aiofiles, os, pytesseract, io

import pandas as pd
import matplotlib.pyplot as plt

from dependencies.oauth2 import get_current_user

upload_file = APIRouter(prefix="/application/version/v1/utilities", tags=['Misc'])

directory_to_save_file = "./files/data/"

@upload_file.post("/upload/file-upload")
async def upload_file_data(request: Request, authorization: str = Depends(get_current_user), file: UploadFile = File(...)):
    async with aiofiles.open(directory_to_save_file + file.filename, "wb") as bufferfile:
        while content := await file.read(1024):  # Read file in chunks
            await bufferfile.write(content)
    return {"info": f"File '{file.filename}' saved successfully"}

@upload_file.get("/upload/list-items")
async def listing_files(request: Request, authorization: str = Depends(get_current_user)):
    try:
        files = os.listdir(directory_to_save_file)
        files = [file for file in files if os.path.isfile(os.path.join(directory_to_save_file, file))]
        retval = {
            "dirpath": directory_to_save_file,
            "files": files
        }
        return retval
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No file was found or not yet to be uploaded")
    

@upload_file.post("/upload/image-to-text")
async def image_to_text(request: Request, file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is not an image")
    try:
        # read the uploaded file
        img_bytes = await file.read()
        img = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(img, lang="eng", config=r'--oem 3 --psm 6')
        
        # Generate a filename based on the uploaded file's name
        filename = f"{os.path.splitext(file.filename)[0]}.txt"
        file_path = os.path.join(directory_to_save_file, filename)

        # Save the extracted text asynchronously
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(text)
        return JSONResponse(content={"img_to_text": text})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occured: {e}")
    