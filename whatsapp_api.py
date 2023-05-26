from flask import Flask, request
from fastapi import FastAPI
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
# Init the Flask App
import requests
from pathlib import Path
global li
li = []

app = Flask(__name__)




@app.route('/whatsapp', methods=['POST'])
def chatgpt():
    global li
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    link = request.values.get('MediaUrl0')
    if link is not None:
       li.append(link)



    if 1==1:
            response = requests.get(li[0])
            pdf = open("metadata.pdf", 'wb')
            pdf.write(response.content)
            pdf.close()
            print("saved",li)
            li=[]
            print("working")
            url = 'https://commonapi.onrender.com/ssebowaAI?query=translate to arabic' #text from user
            file = {'doc': open('metadata.pdf', 'rb')} #image from user
            resp = requests.post(url=url,files=file) 
            print(resp.json())
            
            bot_resp = MessagingResponse()
            msg = bot_resp.message()
            msg.media(resp.json())    
            return str(bot_resp)





    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body("your query")
    return str(bot_resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)

