from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from PIL import Image

import numpy as np
import time





global li
li = []

from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()


@app.post("/whatsapp")
def chat(From: str = Form(...),MediaUrl0:str = Form(...), Body: str = Form(...)):
    if "scan" in Body.lower():
        link = MediaUrl0
        print("scanning")
        name = link.split("/")[-1]+".png"
        img = Image.open(requests.get(link, stream=True).raw)
        if img.mode == 'RGBA':
               img = image.convert('RGB')
        img.save(name)
        print("img saved")
        url = 'https://commonapi.onrender.com/ssebowaAI?query=scan' #text from user
        file = {'img': open(name,'rb')} #image from user
        resp = requests.post(url=url,files=file) 
        print(resp.json())
 
        #bot_resp = MessagingResponse()
        #msg = bot_resp.message()
                #replace the url 
        #msg.media(resp.json())    
        #return str(bot_resp)
        response = MessagingResponse() 
        msg = response.message()
        msg.media(MediaUrl0)
        return Response(content=str(response), media_type="application/xml")

    
    
    
    
    # scanner codes

    

        
                




