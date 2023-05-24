from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
# Init the Flask App
app = Flask(__name__)
openai.api_key = "api-key"

def generate_answer(word):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role":"user","content":word}],

    )
    return response.choices[0].message.content
global li
li = []
@app.route('/whatsapp', methods=['POST'])
def chatgpt():
    global li
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    link = request.values.get('MediaUrl0')
    li.append(link)
    
    if "to pdf" in incoming_que:
        print(li)
        li=[]

    if "translate" in incoming_que:
        import requests
        from pathlib import Path
        filename = Path('metadata.pdf')
        response = requests.get(li[0])
        filename.write_bytes(response.content)
        print("pdf saved",li)

        url = 'https://commonapi.onrender.com/ssebowaAI?query=translate to arabic' #text from user
        file = {'doc': open('metadata.pdf', 'rb')} #image from user
        resp = requests.post(url=url,files=file) 
        print(resp.json())
        li=[]
        bot_resp = MessagingResponse()
        msg = bot_resp.message()
        msg.media(resp.json())    
        return str(bot_resp)

    if "draw" in incoming_que or "design" in incoming_que:
        response = requests.post("https://api.ssebowa.chat/ssebowaAI?query="+incoming_que)
        resp = MessagingResponse()
        msg = resp.message()
        # Add a media response
        imgUrl = eval(response.content.decode("utf-8")).replace("https://commonapi.onrender.com","https://api.ssebowa.chat")
        print(eval(response.content.decode("utf-8")).replace("https://commonapi.onrender.com","https://api.ssebowa.chat"))
        msg.media(imgUrl)
        return str(resp)
    if "sssssssss" in incoming_que:
        # Generate the answer using GPT-3
        #answer = generate_answer(incoming_que)
        print("BOT Answer: ", incoming_que)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body("your query")
    return str(bot_resp)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
