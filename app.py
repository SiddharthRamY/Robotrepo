from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from camera import VideoCamera
from voskk import voice_output, start_voice_thread, stop_voice_thread
from simulation import collision_avoidance_lidar
import os

app = Flask(__name__)
camera_instance = VideoCamera()  # Shared camera instance

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera_instance), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/start_voice_recognition', methods=['POST'])
def start_voice():
    start_voice_thread()
    return jsonify({"status": "started"})

@app.route('/stop_voice_recognition', methods=['POST'])
def stop_voice():
    stop_voice_thread()
    return jsonify({"status": "stopping"})

@app.route('/get_voice_output')
def get_voice_output():
    return jsonify(voice_output)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        front = int(request.form['front'])
        left = int(request.form['left'])
        right = int(request.form['right'])
        result = collision_avoidance_lidar(front, left, right)
    return render_template('app.html', result=result)

@app.route('/set_confidence', methods=['POST'])
def set_confidence():
    try:
        threshold = float(request.form.get('threshold', 0.25))
        camera_instance.set_confidence_threshold(threshold)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/screenshot', methods=['POST'])
def screenshot():
    filename = camera_instance.capture_screenshot()
    return jsonify(success=bool(filename))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('screenshots', filename)

if __name__ == "__main__":
    app.run(debug=True)
