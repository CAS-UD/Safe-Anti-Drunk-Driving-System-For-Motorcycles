from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_cors import CORS
from gevent import monkey
monkey.patch_all()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def connect():
    print("connect")

@socketio.on('disconnect')
def disconnect():
    print("disconnect")
@app.route('/api/send_data', methods=['POST'])
def capture_all_post_requests():
    data = request.get_data(as_text=True)
    socketio.emit('post_req', data)
    return "OK"

if __name__ == '__main__':
    socketio.run(app, debug=True)
