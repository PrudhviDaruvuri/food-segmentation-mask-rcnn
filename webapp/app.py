from fastapi.staticfiles import StaticFiles
import sys
import os
sys.path.insert(0, os.path.realpath(os.path.pardir))
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
import uuid
import logging
import numpy as np
import cv2
import torch
from predict import *
UPLOAD_FOLDER = './uploads'
app = FastAPI()
app.mount("/static", StaticFiles(directory="templates/static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={'request': request})


@app.post('/api/process')
async def process(file: UploadFile = File(...)):
    try:
        name = str(uuid.uuid4()).split('-')[0]
        ext = file.filename.split('.')[-1]
        file_name = f'{UPLOAD_FOLDER}/{name}.{ext}'
        with open(file_name, 'wb+') as f:
            f.write(file.file.read())
        f.close()

        img_tensor, img = prepare_image(file_name)
        with torch.no_grad():
            prediction = model([img_tensor])

        img, results = decode_results(img, prediction)
        output_path = f'images/{name}.{ext}'
        cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        return JSONResponse(status_code=200, content={'output': f'/images/{name}.{ext}', 'result': results})
    except Exception as ex:
        print(ex)
        logging.info(ex)
        return JSONResponse(status_code=400, content={})
