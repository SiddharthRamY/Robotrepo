from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
from voskk import voice_output, start_voice_thread, stop_voice_thread
from simulation import collision_avoidance_lidar

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/get_voice_output')
def get_voice_output():
    return jsonify(voice_output)

@app.route('/start_voice_recognition', methods=['POST'])
def start_voice():
    start_voice_thread()
    return jsonify({"status": "started"})

@app.route('/stop_voice_recognition', methods=['POST'])
def stop_voice():
    stop_voice_thread()
    return jsonify({"status": "stopping"})

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        front = int(request.form['front'])
        left = int(request.form['left'])
        right = int(request.form['right'])
        result = collision_avoidance_lidar(front, left, right)
    return render_template('app.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)

