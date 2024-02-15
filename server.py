from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from gevent import monkey
import Fuzzy_Logic.Fuzzy as FzLo
import json

monkey.patch_all()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
fuzzy = FzLo.Fuzylogic()

@socketio.on('connect')
def connect():
    print("connect")

@socketio.on('disconnect')
def disconnect():
    print("disconnect")
    
@app.route('/api/send_data', methods=['POST'])
def capture_all_post_requests():
    global tiempo_inicio
    global corriendo
    data = request.get_data(as_text=True)
    socketio.emit('post_req', data)
    fuzzy.AsingValue(json.loads(data))
    if float (fuzzy.Calculate()) < 50 and obtener_tiempo_transcurrido() == 0:
        desi = fuzzy.CalculateDesition(float(fuzzy.Calculate), obtener_tiempo_transcurrido())
        if desi[0]:
            tiempo_inicio = 0
            corriendo = False
            return "True"
        elif desi[1]:
            corriendo = True
            return "False"
    return str(fuzzy.Calculate())

if __name__ == '__main__':
    socketio.run(app, debug=True)


import threading
import time

tiempo_inicio = 0
corriendo = True

def actualizar_tiempo_inicio():
    global tiempo_inicio
    while corriendo:
        tiempo_inicio = time.time()
        time.sleep(1) 

def obtener_tiempo_transcurrido():
    return time.time() - tiempo_inicio


hilo = threading.Thread(target=actualizar_tiempo_inicio)

hilo.start()


