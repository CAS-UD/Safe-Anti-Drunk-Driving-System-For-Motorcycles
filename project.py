from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('post_request')
def handle_post_request(data):
    content = data.get('content', '')
    print(f"Data received: {content}")
    socketio.emit('post_request_response', {'content': f"Respuesta del servidor: {content}"})

@app.route('/', methods=['POST'])
def capture_all_post_requests():
    data = request.get_data(as_text=True)
    print(f"Capturada solicitud POST: {data}")
    socketio.emit('post_request_response', {'content': f"Capturada solicitud POST: {data}"})
    return "OK"

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
