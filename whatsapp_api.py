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

@app.route('/whatsapp', methods=['POST','GET'])
def chatgpt():

    return "working"
    if "draw" in incoming_que or "design" in incoming_que:
        response = requests.post("https://api.ssebowa.chat/ssebowaAI?query="+incoming_que)
        resp = MessagingResponse()
        msg = resp.message()
        # Add a media response
        imgUrl = eval(response.content.decode("utf-8")).replace("https://commonapi.onrender.com","https://api.ssebowa.chat")
        print(eval(response.content.decode("utf-8")).replace("https://commonapi.onrender.com","https://api.ssebowa.chat"))
        msg.media(imgUrl)
        return str(resp)
    else:
        # Generate the answer using GPT-3
        answer = generate_answer(incoming_que)
        print("BOT Answer: ", answer)
        bot_resp = MessagingResponse()
        msg = bot_resp.message()
        msg.body(answer)
        return str(bot_resp)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
