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
       filename = Path('metadata.pdf')
       response = requests.get(li[0])
       filename.write_bytes(response.content)
       print("saved",li)


    if "trans" in incoming_que:
        print("working")
        try:
            url = 'https://commonapi.onrender.com/ssebowaAI?query='+incoming_que #text from user
            file = {'doc': open('metadata.pdf', 'rb')} #image from user
            resp = requests.post(url=url,files=file) 
            print(resp.json())
            li=[]
            bot_resp = MessagingResponse()
            msg = bot_resp.message()
            msg.media(resp.json())    
            return str(bot_resp)
        except:
            print("error re trying.....")




    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body("your query")
    return str(bot_resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)

