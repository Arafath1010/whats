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
import csv
import json
import requests
import json
headers = {"Authorization": f"Bearer {'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'}"}
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
from PyPDF2 import PdfReader
@app.post("/whatsapp")
async def chat(From: str = Form(...),MediaUrl0:str = Form(None), Body: str = Form(None)):
        def load_csv_data(csv_file):
            with open(csv_file, "r") as file:
                reader = csv.reader(file)
                table = list(reader)
            return table
        
        def convert_table_to_dict(table):
            headers = table[0]
            data = table[1:]
            table_dict = {header: [] for header in headers}
            for row in data:
                for i, value in enumerate(row):
                    table_dict[headers[i]].append(value)
            return table_dict
        
        def query(payload):
            headers = {"Authorization": f"Bearer {'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'}"}
            API_URL = "https://api-inference.huggingface.co/models/google/tapas-base-finetuned-wtq"
            data = json.dumps(payload)
            response = requests.request("POST", API_URL, headers=headers, data=data)
            return json.loads(response.content.decode("utf-8"))
            
        if MediaUrl0 is not None:
            response = requests.get(MediaUrl0)
            file = open(From, 'wb')
            file.write(response.content)
            file.close()
            print("file saved",MediaUrl0)
            response = MessagingResponse() 
            msg = response.message()
            msg.body("please ask question to anlyze your data !")
            return Response(content=str(response), media_type="application/xml")
        try:
            csv_file = From  # is a file name
            table = load_csv_data(csv_file)
            table_dict = convert_table_to_dict(table)
        except:
            data_frame = pd.read_excel(From)
            data_frame.to_csv(From, index=False)
            csv_file = From  # is a file name
            table = load_csv_data(csv_file)
            table_dict = convert_table_to_dict(table)
    
        payload = {
            "inputs": {
                "query": Body,
                "table": table_dict,
            }
        }
        
        data = query(payload)
        print(data)

        response = MessagingResponse() 
        msg = response.message()
        #msg.media("https://whatsapp-vz43.onrender.com/static/"+name)
        try: 
            msg.body(data['answer'])
        except:
            msg.body("please recheck the question !")
        return Response(content=str(response), media_type="application/xml")
    

    
    
    
    
    # scanner codes

'''
    #if "count" in Body.lower():
       # link = MediaUrl0
    
    def read_pdf_from_url(url):
        if MediaUrl0 is not None:
            response = requests.get(url)
            file = open('temp.pdf', 'wb')
            file.write(response.content)
            file.close()
            print("file saved")
        reader = PdfReader("temp.pdf")
        number_of_pages = len(reader.pages)
        text = ""
        for i in range(number_of_pages):
          page = reader.pages[i]
          text = text + page.extract_text()
        return text.replace('\n'," ")


    # Provide the URL of your PDF file
    pdf_url = MediaUrl0
    pdf_content = read_pdf_from_url(pdf_url)
    #print(pdf_content)
    resp = "ask your Question"
    if Body is not None:
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
        print(Body)'''

        
                




