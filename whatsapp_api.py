from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from PIL import Image
import cv2
import imutils
import numpy as np
import time




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
    
    
    
    
    
    # scanner codes

    
    if "scan" in incoming_que:
        print("scanning")
        name = link.split("/")[-1]+".png"
        img = Image.open(requests.get(link, stream=True).raw)
        if img.mode == 'RGBA':
               img = image.convert('RGB')
        img.save(name)

        def order_points(pts):
            """Rearrange coordinates to order:
               top-left, top-right, bottom-right, bottom-left"""
            rect = np.zeros((4, 2), dtype='float32')
            pts = np.array(pts)
            s = pts.sum(axis=1)
            # Top-left point will have the smallest sum.
            rect[0] = pts[np.argmin(s)]
            # Bottom-right point will have the largest sum.
            rect[2] = pts[np.argmax(s)]
        
            diff = np.diff(pts, axis=1)
            # Top-right point will have the smallest difference.
            rect[1] = pts[np.argmin(diff)]
            # Bottom-left will have the largest difference.
            rect[3] = pts[np.argmax(diff)]
            # return the ordered coordinates
            return rect.astype('int').tolist()
    
    
        def scan(img):
            # Resize image to workable size
            dim_limit = 1080
            max_dim = max(img.shape)
            if max_dim > dim_limit:
                resize_scale = dim_limit / max_dim
                img = cv2.resize(img, None, fx=resize_scale, fy=resize_scale)
        
            # Create a copy of resized original image for later use
            orig_img = img.copy()
            # cv2.imshow("original_resized", orig_img)
        
            # Repeated Closing operation to remove text from the document.
            kernel = np.ones((5, 5), np.uint8)
            img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=3)
            # cv2.imshow("morphologyEX", img)
        
            # GrabCut
            mask = np.zeros(img.shape[:2], np.uint8)
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)
            rect = (20, 20, img.shape[1] - 20, img.shape[0] - 20)
            cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            img = img * mask2[:, :, np.newaxis]
            # cv2.imshow("grabcut", img)
        
            # Convert to grayscale.
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (11, 11), 0)
            # cv2.imshow("gray_blurred", gray)
        
            # Edge Detection.
            canny = cv2.Canny(gray, 0, 200)
            canny = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
            # cv2.imshow("canny_dilate", canny)
        
            # Finding contours for the detected edges.
            contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            # Keeping only the largest detected contour.
            page = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        
            # Detecting Edges through Contour approximation.
            # Loop over the contours.
            if len(page) == 0:
                return orig_img
            for c in page:
                # Approximate the contour.
                epsilon = 0.02 * cv2.arcLength(c, True)
                corners = cv2.approxPolyDP(c, epsilon, True)
                # If our approximated contour has four points.
                if len(corners) == 4:
                    break
        
            # Sorting the corners and converting them to desired shape.
            corners = sorted(np.concatenate(corners).tolist())
            # For 4 corner points being detected.
            # Rearranging the order of the corner points.
            corners = order_points(corners)
            (tl, tr, br, bl) = corners
        
            # Draw points
            points_img = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
            point_count = 0
            for corner in corners:
                cv2.circle(points_img, corner, 3, (255, 0, 0), -1)
                point_count += 1
                cv2.putText(points_img, str(point_count), corner, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # cv2.imshow("points", points_img)
        
            # Finding the maximum width.
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))
        
            # Finding the maximum height.
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))
        
            # Final destination co-ordinates.
            destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxHeight], [0, maxHeight]]
        
            # Getting the homography.
            M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))
            # Perspective transform using homography.
            final = cv2.warpPerspective(orig_img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
        
            return final


        #runtime = []
        for img_path in ["image"]:
           
                img = cv2.imread(name)
                print(img_path)
                print(type(img))
                t1 = time.time()
        
                scanned_img = scan(img)
        
                t2 = time.time()
        
                #runtime.append({'image': img_path, 'time': t2 - t1})
        
                #cv2.imshow("scanner", scanned_img)
                cv2.imwrite('static/' + name, scanned_img)
                print("scanned"+name)
        
                



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)

