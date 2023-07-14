from flask import Flask, request
#torch
#transformers
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from PIL import Image
#import cv2
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
#import cvlib as cv
#from cvlib.object_detection import draw_bbox

import numpy as np
import time





global li
li = []

from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse


#from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

#model_name = "deepset/roberta-base-squad2"

# a) Get predictions
#nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/static", response_class=HTMLResponse)
def list_files(request: Request):

    files = os.listdir("./static")
    files_paths = sorted([f"{request.url._url}/{f}" for f in files])
    print(files_paths)
    return templates.TemplateResponse(
        "list_files.html", {"request": request, "files": files_paths}
    )

import requests

import json
headers = {"Authorization": f"Bearer {'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'}"}
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
import PyPDF2
@app.post("/whatsapp")
async def chat(From: str = Form(...),MediaUrl0:str = Form(None), Body: str = Form(None)):
    #if "count" in Body.lower():
       # link = MediaUrl0
    
    def read_pdf_from_url(url):
        if MediaUrl0 is not None:
            response = requests.get(url)
            file = open('temp.pdf', 'wb')
            file.write(response.content)
            file.close()
            print("file saved")
    
        with open('temp.pdf', 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            content = ''
            
            for page_num in range(num_pages):
                page = reader.getPage(page_num)
                content += page.extractText()
            print("contend return")
            return content

    # Provide the URL of your PDF file
    pdf_url = MediaUrl0
    pdf_content = read_pdf_from_url(pdf_url)
    #print(pdf_content)
    def model_response(question):
        def query(payload):
            data = json.dumps(payload)
            response = requests.request("POST", API_URL, headers=headers, data=data)
            return json.loads(response.content.decode("utf-8"))
        data = query(
            {
                "inputs": {
                    "question": question,
                    "context": str(pdf_content),
                }
            }
        )

        return str(data)
    print(Body)
    resp = model_response(str(Body))
    


    response = MessagingResponse() 
    msg = response.message()
    #msg.media("https://whatsapp-vz43.onrender.com/static/"+name)
    msg.body(resp)
    return Response(content=str(response), media_type="application/xml")

    
    
    
    
    # scanner codes

    

        
                




