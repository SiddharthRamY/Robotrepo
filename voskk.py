import sounddevice as sd
import queue
import sys
import json
from vosk import Model, KaldiRecognizer
import threading

voice_output = {"text": ""}
voice_thread_running = [False]
voice_stop_flag = [False]
voice_thread = None

def start_voice_recognition(output_dict=voice_output, running_flag=voice_thread_running, stop_flag=voice_stop_flag):
    running_flag[0] = True
    model = Model(r"D:\push_logger\voskmodel")  # Update this path as needed!
    rec = KaldiRecognizer(model, 16000)
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        try:
            while True:
                if stop_flag[0]:
                    break
                try:
                    data = q.get(timeout=0.1)
                except queue.Empty:
                    continue
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    output_dict["text"] = result.get("text", "")
        except Exception as e:
            print("Voice recognition error:", e, file=sys.stderr)
        finally:
            running_flag[0] = False
            output_dict["text"] = "Voice recognition stopped."

def start_voice_thread():
    global voice_thread
    if not voice_thread_running[0]:
        voice_stop_flag[0] = False
        voice_thread = threading.Thread(
            target=start_voice_recognition,
            args=(voice_output, voice_thread_running, voice_stop_flag)
        )
        voice_thread.daemon = True
        voice_thread.start()

def stop_voice_thread():
    voice_stop_flag[0] = True
