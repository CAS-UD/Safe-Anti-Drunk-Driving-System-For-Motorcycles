import json
import time


def verificar_inclinacion(data):
    data = data.replace('\r', '').replace('\n', '')
    try:
        data = json.loads(data)
        print(data)
        # Procesar los datos como antes
        for euler_data in data["Euler"]:
            print(euler_data[0])
            print(euler_data[1])
            euler_x = euler_data[0]  # Ángulo alrededor del eje X
            euler_y = euler_data[1]  # Ángulo alrededor del eje Y

            # Umbrales para inclinación
            umbral_x = 45  # grados
            umbral_y = 45  # grados

            # Verificación de inclinación
            inclinacion_x = abs(euler_x) > umbral_x
            inclinacion_y = abs(euler_y) > umbral_y

            if inclinacion_x:
                return "IMU demasiado inclinado hacia adelante/atrás (eje X)."
            elif inclinacion_y:
                return "IMU demasiado inclinado hacia la derecha/izquierda (eje Y)."
            else:
                return "IMU en una posición aceptable."
    except:
        return "[!] ERROR with Data collected!!!"

