import cv2
import numpy as np
from keras.models import model_from_json
from flask import Flask, render_template, Response,jsonify
# from keras.models import model_from_json
# from flask import Flask, render_template, Response
import threading  # Import the threading module
import subprocess 
from datetime import datetime
# from botify import chatbot
import speech_recognition as sr
import random
from textblob import TextBlob
import os
import signal
from gtts import gTTS
import playsound
app = Flask(__name__)
import threading
audio_process = None 
camera_thread_running = threading.Event()
bot_thread_running = threading.Event()
camera_thread = None  # Initialize camera thread
bot_thread = None  
mouth_cascade = cv2.CascadeClassifier('E:/Mini Project/Smile-Detection-and-Smile-Count-master/haarcascade_smile.xml')

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# Load json and create model
json_file = open('E:/Mini Project/Emotion_detection_with_CNN-main/model/emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# Load weights into the model
emotion_model.load_weights("E:/Mini Project/Emotion_detection_with_CNN-main/model/emotion_model.h5")
print("Loaded model from disk")

font = cv2.FONT_HERSHEY_SIMPLEX

# Capture video from the camera
cap = cv2.VideoCapture(0)

def speak_text(text):
    # global audio_process
    tts = gTTS(text=text, lang='en')
    date_string = datetime.now().strftime("%M%S")
    filename = date_string+".mp3"
    tts.save(filename)
    playsound.playsound(filename)
    # audio_process = subprocess.Popen(["mpg123", filename])

    # bot_thread_running = False
def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""

def chatbot():
    global sum 
    global sum1 
    sum=0
    sum1=0
    t1='Hello, thank you for coming in, I am here to support you. To get started, Could you please share your name with me?'
    t=speak_text(t1)
    name = speech_to_text()  # Input name directly
    print('')
    z='Nice to meet you'  + name
    z1=speak_text(z)
    # Greeting random selection and polarity-based response
    questions = [
        'So ' + name + 'How are you feeling today?',
        'So' + name + 'Can you tell me a bit about what has been going on in your life lately?',
        'So ' + name + 'Is there something specific you would like to talk about during our session?',
        'Greetings' + name + 'What brings you in to see me today?',
        'So ' + name + ' How are things going in your life?'
    ]

    o=random.choice(questions)
    o1=speak_text(o)
    ans = speech_to_text()
    print('')
    blob = TextBlob(ans)
    if blob.polarity > 0:
        m='I am glad that you are well'
        m1=speak_text(m)
    else:
        m= name+ "that doesn't sound so good"
        m1=speak_text(m)

    # Random question on a random topic
    topics = [
        'your family relationships?',
        'your social interactions?',
        'your personal achievements?',
        'your sleep patterns?',
        'your coping mechanisms?',
        'your self-esteem?',
        'the stress you experience at work or school?',
        'your body image?',
        'the changes in your daily routine?',
        'the impact of past traumas on your current mental state?',
        'the impact of unresolved conflicts on your mental health?.',
        'your ability to express your emotions?',
        'your self worth?',
        'your personal well-being?',
        'your daily emotions and challenges?'
    ]

    questions = [
        'What is your take on ',
        'What do you think about ',
        'How do you feel about ',
         name + ' Do you like ',
        'I would like to know your opinion on ',
        'I would love to know what you think about ' 
    ]

    for i in range(0,3):
        topic = random.choice(topics)
        topics.remove(topic)
        question = random.choice(questions)
        questions.remove(question)
        x=(question + topic + '?')
        x1=speak_text(x)

        # Response to random question using sentiment analysis
        ans = speech_to_text()
        print('')
        blob = TextBlob(ans)

        # Respond appropriately to positive and negative sentiment
        if blob.polarity > 0.5:
            a = 'Wow you really love ' + topic
        elif blob.polarity > 0.1:
            a = 'Cool you like ' + topic
        elif blob.polarity < -0.1:
            a = 'Hmm, so you are not a fan of ' + topic
        elif blob.polarity < -0.5:
            a = 'So you hate ' + topic
        else:
            a = 'That is a very neutral view on ' + topic

        if blob.subjectivity > 0.6:
            m= (a + ' and you are totally biased')
            m1=speak_text(m)
        elif blob.subjectivity > 0.3:
            m=(a + ' and you are a bit biased')
            m1=speak_text(m)
        else:
            m=(a + ' and quite objective')
            m1=speak_text(m)
        sum=sum+blob.polarity
        sum1=sum1+blob.subjectivity
    if(sum>1.4):  
        if(sum1>1.8):                
            m=('You have a good mental state and is strongly inclined towards your thoughts')
            m1=speak_text(m)
        else:
            m=('You are in a positive mental state and is quite objective with thoughts')
            m1=speak_text(m)
    
    elif(sum<-1.8):
        if(sum1>1.8):                
            m=('You have a not soo good mental state and is strongly inclined towards your thoughts')
            m1=speak_text(m)
        else:
            m=('You are in a negative mental state and is quite objective with thoughts')
            m1=speak_text(m)
    else:
        if(sum1>1.8):                
            m=('You have a stable mental state and is strongly inclined towards your thoughts')
            m1=speak_text(m)
        else:
            m=('You are in a neutral mental state and is quite objective with thoughts')
            m1=speak_text(m)
    print(sum,"  -  ",sum1)




    # Random goodbye
    goodbyes = [
        'Thank you for sharing your thoughts today' + name + 'Remember, I am here for you whenever you need to talk',
        'As we wrap up, remember that your journey to self-improvement is ongoing' + name + 'I am here to support you every step of the way',
        'I am glad we had this time to talk' + name + 'Remember, I am here to support you, and I look forward to our next session',
        'Our session is ending, but your path to healing is ongoing. Until next time, take moments to reflect on your strengths and growth',
        'I appreciate your openness during our session' + name + 'Remember that your well-being is a priority, and I am here whenever you are ready to talk',
        'Our session is ending, but your growth continues. Embrace the progress you have made and know that I am here to support you moving forward',
    ]

    b=(random.choice(goodbyes))
    b1=speak_text(b)


def detect_emotions():
    while True:
        # Read frame from the camera
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1050, 700))
        rows, cols, _ = frame.shape

        if not ret:
            break

        face_detector = cv2.CascadeClassifier(
            'E:/Mini Project/Emotion_detection_with_CNN-main/haarcascades/haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        num_faces = face_detector.detectMultiScale(gray_frame, 1.3, 5)
        cv2.putText(frame, "Number of faces detected: " + str(len(num_faces)), (40, 40), font, 1, (155, 175, 0), 2)

        count = 0

        # Process each face detected
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (60, 64, 151), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            sm = mouth_cascade.detectMultiScale(roi_gray_frame)
            count += 1
            cv2.putText(frame, "Number of Smile Count: " + str(count), (40, 600), font, 1, (5, 25, 0), 2)
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            cv2.putText(frame, emotion_dict[maxindex], (x + 5, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (251, 25, 120), 2, cv2.LINE_AA)

            # Draw rectangle based on detected emotion
            if emotion_dict[maxindex] == "Sad":
                percentage_blinking = 10 / 100
                loading_x = int(cols * percentage_blinking)
                cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (0, 0, 220), -1)
            elif emotion_dict[maxindex] == "Angry":
                percentage_blinking = 30 / 100
                loading_x = int(cols * percentage_blinking)
                cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (10, 70, 240), -1)
            elif emotion_dict[maxindex] == "Disgusted":
                percentage_blinking = 15 / 100
                loading_x = int(cols * percentage_blinking)
                cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (20, 201, 11), -1)
            elif emotion_dict[maxindex] == "Fearful":
                percentage_blinking = 35 / 100
                loading_x = int(cols * percentage_blinking)
                cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (0, 51, 251), -1)
            elif emotion_dict[maxindex] == "Happy":
                percentage_blinking = 100 / 100
                loading_x = int(cols * percentage_blinking)
                cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (1, 200, 1), -1)
            elif emotion_dict[maxindex] == "Neutral":
                percentage_blinking = 52 / 100
                loading_x = int(cols * percentage_blinking)
                cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (0, 251, 251), -1)
            elif emotion_dict[maxindex] == "Surprised":
                percentage_blinking = 60 / 100
                loading_x = int(cols * percentage_blinking)
                cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (75, 151, 51), -1)
        
        # Convert frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        # Yield the frame as a response to the client
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def run_camera():
    global camera_thread_running
    while camera_thread_running.is_set():
        frame = detect_emotions()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def run_bot():
    global bot_thread_running
    bot_thread_running.set()
    chatbot()
    bot_thread_running.clear()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(detect_emotions(), mimetype='multipart/x-mixed-replace; boundary=frame')
# ... (rest of your code)

@app.route('/start_camera', methods=['GET'])
def start_camera():
    global camera_thread_running, bot_thread_running, camera_thread, bot_thread
    if not camera_thread_running.is_set():
        camera_thread_running.set()
        camera_thread = threading.Thread(target=run_camera)
        camera_thread.start()

    # Start both camera and chatbot threads simultaneously
    if not bot_thread_running.is_set():
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.start()

    # Play sound
    t1 = "Camera is now open. Please start speaking."
    speak_text(t1)

    return jsonify(message="Camera and chatbot started")

# # ... (other parts of your app.py code)
import os  # Import the os module

# ... (other parts of your app.py code)

@app.route('/stop_camera', methods=['GET'])
def stop_camera():
    global camera_thread_running, bot_thread_running, camera_thread, bot_thread, audio_process

    if camera_thread and camera_thread_running.is_set():
        camera_thread_running.clear()
        camera_thread.join()

    if bot_thread and bot_thread_running.is_set():
        bot_thread_running.clear()
        bot_thread.join()

    # Stop the audio process if it's running
    if audio_process:
        os.kill(audio_process.pid, signal.SIGTERM)
        audio_process = None  # Reset the audio process variable

    return jsonify(message="Camera and audio have been stopped")

if __name__ == '__main__':
    app.run(debug=True)