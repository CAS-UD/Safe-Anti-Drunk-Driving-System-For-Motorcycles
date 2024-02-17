from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from gevent import monkey
import Fuzzy_Logic.Fuzzy as FzLo
import time
import json
import threading

monkey.patch_all()

tiempo_inicio = 0
estado = 0
est = False

def VerifyTime():
    while True:
        if estado <= 0:
            actualizar_tiempo_inicio()
        time.sleep(1)

def actualizar_tiempo_inicio():
    global tiempo_inicio
    tiempo_inicio = time.time()

def obtener_tiempo_transcurrido():
    return round(time.time() - tiempo_inicio)

threading.Thread(target=VerifyTime).start()

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
    global estado
    global est
    data = request.get_data(as_text=True)
    socketio.emit('post_req', data)
    fuzzy.AsingValue(json.loads(data))
    fuzzy_cal = round(float(fuzzy.Calculate()),3)
    if est:
        return "True"
    else:
        if fuzzy_cal < 75:
            obtener_tiempo_transcurrido()
            if estado <= 0:
                actualizar_tiempo_inicio()
                estado += 1
                return "False"
            if estado >= 5:
                actualizar_tiempo_inicio()
                estado = 0
                est = True
                return "True"
            if obtener_tiempo_transcurrido() >= 30:
                estado = 0
                actualizar_tiempo_inicio()
                return "False"
            if estado > 0 and obtener_tiempo_transcurrido() < 30:
                estado += 1
                return "False"
        else: 
            if estado >= 5:
                actualizar_tiempo_inicio()
                estado = 0
                est = True
                return "True"
            if estado > 0 and obtener_tiempo_transcurrido() < 30:
                return "False"
            if obtener_tiempo_transcurrido() >= 30:
                estado = 0
                actualizar_tiempo_inicio()
                return "False"
            if estado <= 0:
                actualizar_tiempo_inicio()
                return "False"

if __name__ == '__main__':
    socketio.run(app, debug=True)



