from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from PIL import Image
import cv2
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request


import numpy as np
import time





global li
li = []

from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse

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

@app.post("/whatsapp")
async def chat(From: str = Form(...),MediaUrl0:str = Form(...), Body: str = Form(...)):
    if "count" in Body.lower():
        link = MediaUrl0
        print("counting")
        name = link.split("/")[-1]+".png"
        img = Image.open(requests.get(link, stream=True).raw)
        if img.mode == 'RGBA':
               img = image.convert('RGB')
        img.save(name)
        print("img saved")
        img.close()
        
        image = cv2.imread(name)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        
        blur = cv2.GaussianBlur(gray, (11,11), 0)
        
        
        canny = cv2.Canny(blur, 30, 150, 3)
        
        
        dilated = cv2.dilate(canny, (1,1), iterations = 2)
        (cnt, heirarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.drawContours(rgb, cnt, -1, (0,255,0), 1)
        cv2.imwrite("static/"+name ,rgb)
        print('Count: ', len(cnt)-len(cnt)//2)

        
        #url = 'https://commonapi.onrender.com/ssebowaAI?query=scan' #text from user
        #file = {'img': open(name,'rb')} #image from user
        #resp = requests.post(url=url,files=file) 
        #print(resp.json())
 
        #bot_resp = MessagingResponse()
        #msg = bot_resp.message()
                #replace the url 
        #msg.media(resp.json())    
        #return str(bot_resp)
        response = MessagingResponse() 
        msg = response.message()
        msg.media("https://whatsapp-vz43.onrender.com/static/"+name)
        msg.body('Count: '+str(len(cnt)-len(cnt)//2))
        return Response(content=str(response), media_type="application/xml")

    
    
    
    
    # scanner codes

    

        
                




