from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
#from PIL import Image
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




from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
import requests
import csv
import json
import requests
import json
import pandas as pd
import io

from hugchat import hugchat
from hugchat.login import Login

# Log in to huggingface and grant authorization to huggingchat
sign = Login("arafathbict@gmail.com", "Bict@100")
cookies = sign.login()

# Create a ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"
bot_message = chatbot.chat("hi")

app = FastAPI()



@app.post("/whatsapp")
async def chat(From: str = Form(...),MediaUrl0:str = Form(None), Body: str = Form(None)):
            
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

        csv_file_path = From
        csv_output = io.StringIO()
        with open(csv_file_path, "r", encoding="latin-1") as file:
                    csv_reader = csv.reader(file)
                    csv_writer = csv.writer(csv_output)
                    csv_writer.writerows(csv_reader)
        csv_string = csv_output.getvalue()

        
        bot_message = chatbot.chat(csv_string+"  "+Body)
        bot_message

        response = MessagingResponse() 
        msg = response.message()
        #msg.media("https://whatsapp-vz43.onrender.com/static/"+name)
        try: 
            msg.body(bot_message)
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

        
                




