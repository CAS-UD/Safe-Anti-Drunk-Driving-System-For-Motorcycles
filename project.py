from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
import json
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    return json.dumps({'client_status': True})

@app.route('/api', methods=['POST'])
def capture_all_post_requests():
    data = request.get_data(as_text=True)
    print(f"Capturada solicitud POST: {data}")
    socketio.emit('post_request_response', data)
    return "OK"

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
