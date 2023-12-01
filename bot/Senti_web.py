import cv2
import numpy as np
from keras.models import model_from_json
from flask import Flask, render_template, Response
from botify import chatbot
app = Flask(__name__)

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
            chatbot()
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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(detect_emotions(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)