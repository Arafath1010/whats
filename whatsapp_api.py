from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
# Init the Flask App
from PIL import Image
import cv2
import imutils
from transform import perspective_transform


global li
li = []

app = Flask(__name__)




@app.route('/whatsapp', methods=['POST'])
def chatgpt():
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
    
    if "scan" in incoming_que:
        print("scanning")
        name = link.split("/")[-1]+".png"
        img = Image.open(requests.get(link, stream=True).raw)
        if img.mode == 'RGBA':
               img = image.convert('RGB')

        open_cv_image = np.array(img)
        # Passing the image path
        original_img = open_cv_image
        copy = original_img.copy()

        # The resized height in hundreds
        ratio = original_img.shape[0] / 500.0
        img_resize = imutils.resize(original_img, height=500)

        gray_image = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)

        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        edged_img = cv2.Canny(blurred_image, 75, 200)

        cnts, _ = cv2.findContours(edged_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        try:
            for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                if len(approx) == 4:
                    doc = approx
                    break

            p = []

            for d in doc:
                tuple_point = tuple(d[0])
                cv2.circle(img_resize, tuple_point, 3, (0, 0, 255), 4)
                p.append(tuple_point)

            warped_image = perspective_transform(copy, doc.reshape(4, 2) * ratio)
            warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)

            #T = threshold_local(warped_image,21, offset=10, method="gaussian")
            #warped = (warped_image > T).astype("uint8") * 255
            cv2.imwrite("static/"+name,warped_image)
            print("https://whatsapp-vz43.onrender.com/static/"+name)
            bot_resp = MessagingResponse()
            msg = bot_resp.message()
            #replace the url 
            msg.media("https://whatsapp-vz43.onrender.com/static/"+name)    
            return str(bot_resp)
            #return "http://127.0.0.1:8000/static/output/scan-"+name
        except:
            print("image have no borders so try to upload image with borders")
            bot_resp = MessagingResponse()
            msg = bot_resp.message()
            #replace the url 
            msg.text("image have no borders so try to upload image with borders")    
            return str(bot_resp)
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)

