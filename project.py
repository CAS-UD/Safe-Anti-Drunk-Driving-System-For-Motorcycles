from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from FuzzyLogic import verificar_inclinacion

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

#Del lado de la petición
@app.route('/', methods=['POST'])
def capture_all_post_requests():
    data = request.get_data(as_text=True)
    print(f"Capturada solicitud POST: {data}")
    inclinacion_result = verificar_inclinacion(data)
    response_data = {
        'content': data,
        'verificacion': inclinacion_result
    }
    socketio.emit('post_request_response', response_data)
    return jsonify(response_data)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)