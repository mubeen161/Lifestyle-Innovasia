from flask import Flask, render_template, Response
import cv2
import pyaudio
import numpy as np

app = Flask(__name__)

camera = cv2.VideoCapture(0)

# Configure audio settings
audio = pyaudio.PyAudio()
input_stream = audio.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=44100,
                          input=True,
                          frames_per_buffer=1024)

output_stream = audio.open(format=pyaudio.paInt16,
                           channels=1,
                           rate=44100,
                           output=True,
                           frames_per_buffer=1024)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Capture audio data
        audio_data = input_stream.read(1024, exception_on_overflow=False)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
        # Process audio data (e.g., mix with a generated sine wave)
        sine_wave = np.sin(2 * np.pi * 440 * np.arange(0, len(audio_array)) / 44100) * 1000
        mixed_audio = (audio_array + sine_wave).astype(np.int16)
        
        # Process frames and audio data as needed
        # For example, you can combine the audio and video frames and encode them to a video stream
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Send mixed audio back to the user
        output_stream.write(mixed_audio.tobytes())
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # You can create an HTML template for the video display

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
















