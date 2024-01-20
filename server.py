from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/api', methods=['POST'])
def capture_all_post_requests():
    data = request.get_data(as_text=True)
    print(f"Capturada solicitud POST: {data}")
    socketio.emit('message', data)
    return "OK"


if __name__ == '__main__':
    socketio.run(app, debug=True)
