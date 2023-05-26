from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
# Init the Flask App
import requests
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



    if "trans" in incoming_que:
            print("working")
            try:
                url = 'https://commonapi.onrender.com/whatstranslate?link='+li[0]+'&lang=arabic' #text from user
                resp = requests.post(url=url) 
                print(resp.json())
            except:
                print("error")
            
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

