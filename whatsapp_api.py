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
async def chat(From: str = Form(...), Body: str = Form(...)):
   bot_resp = MessagingResponse() 

   msg = bot_resp.message()

   msg.body("https://whatsapp-vz43.onrender.com/static/"+Body)    
   return str(bot_resp)
   #return Response(content=str(response), media_type="application/xml")



    global li
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    link = request.values.get('MediaUrl0')
    print(link)
    if link is not None:
       li.append(link)

    if "to pdf" in incoming_que:
        print("converting")
        images=[]
        for url in li:
            image = Image.open(requests.get(url, stream=True).raw)

            if image.mode == 'RGBA':
               image = image.convert('RGB')
            images.append(image)
        
        
        
        name = url.split("/")[-1]+".pdf"
        if len(li)==1:
           images[0].save("static/"+name, "PDF" ,resolution=100.0, save_all=True)
        else:
           images[0].save("static/"+name, "PDF" ,resolution=100.0, save_all=True,append_images=images[1:])
        li=[]
        print("https://whatsapp-vz43.onrender.com/static/"+name)
        bot_resp = MessagingResponse()
        msg = bot_resp.message()
        #replace the url 
        msg.media("https://whatsapp-vz43.onrender.com/static/"+name)    
        return str(bot_resp)
    
    
    
    
    
    # scanner codes

    
    if "scan" in incoming_que:
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
 
        bot_resp = MessagingResponse()
        msg = bot_resp.message()
                #replace the url 
        msg.media(resp.json())    
        return str(bot_resp)
        
                




