from flask import Flask, Response
import cv2
import gtts, playsound, os
import emoji
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import urllib.request as urlib
import keyboard
app = Flask(__name__)
video = cv2.VideoCapture(0)

count = 0
command = ""
tts = gtts.gTTS("Turn left", tld="co.nz")
fn_left = "turnleft.mp3"
tts.save(fn_left)
tts = gtts.gTTS("Turn right", tld="co.nz")
fn_right = "turnright.mp3"
tts.save(fn_right)
tts = gtts.gTTS("Go forward", tld="co.nz")
fn_forward = "goforward.mp3"
tts.save(fn_forward)

@app.route('/')
def index():
    return "Default Message"

def draw_emoji(image, emoji=':left_arrow:'):
    # font issue
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    tick=str(emoji.emojize(emoji))
    font = ImageFont.truetype("Arial Unicode.ttf",32)
    draw.text((40, 80),tick,(255,255,255),font=font)
    image = np.array(image)
    return image

URL = "http://172.20.10.5:8080/shot.jpg?rnd=493155"

def gen(video):
    while True:
        global count
        global command
        response = urlib.urlopen(URL)
        #response_numpy = np.array(response)
        # read image as an numpy array
        image = np.asarray(bytearray(response.read()), dtype="uint8")
        
        # use imdecode function
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        #success, image = video.read()
        frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)

        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(image, command, (100, 100), font, 3, (255, 255, 255), 3)
        # if count % 200 < 100:
        #      cv2.putText(image, "Turn left!", (100, 100), font, 3, (255, 255, 255), 3)
        #      #image = draw_emoji(image)
        # else:
        #      cv2.putText(image, "Turn right!", (100, 100), font, 3, (255, 255, 255), 3)
        
        if count % 100 == 0:

            try:  # used try so that if user pressed other than the given key error will not be shown
                if keyboard.is_pressed('a'):
                    playsound.playsound(fn_left)
                    command = "Turn left!"
                if keyboard.is_pressed('d'):
                    playsound.playsound(fn_right)
                    command = "Turn right!"
                if keyboard.is_pressed('w'):
                    playsound.playsound(fn_forward)
                    command = "Go forward!"
            except:
                pass
        # if count % 200 == 100:
        #     playsound.playsound(fn_right)

        ret, jpeg = cv2.imencode('.jpg', image)

        frame = jpeg.tobytes()
        count += 1
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)