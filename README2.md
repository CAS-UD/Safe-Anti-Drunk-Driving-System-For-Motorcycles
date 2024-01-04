# Manejo y Envío de Datos con ESP32

Este proyecto tiene como objetivo demostrar el manejo y envío de datos utilizando el ESP32, un microcontrolador ampliamente utilizado en aplicaciones IoT. En este caso, se están realizando pruebas con un sensor de ultrasonido para capturar datos de distancia y luego organizarlos para su posterior envío.

## Contenido

- [Sensores Utilizados](#sensores-utilizados)
- [Configuración del Proyecto](#configuración-del-proyecto)
- [Avances](#avances)
- [Links De Interes](#links)

## Sensores Utilizados

En este proyecto, se está utilizando de momento un sensor de ultrasonido (HC-SR04) para medir distancias. se tiene conectado el pin vcc del sensor al la salida 5V (Pin VIN), el pin trigger al GPIO5, el pin echo al GPIO18 y Gnd a GND, junto con esto una resistencia de 1KOhm en el pin echo.

## Configuración del Proyecto

Asegurese de tener python 3.8 o una version superior, junto con esto instalada la libreria AMPY, en caso de no ternerla instalar introducir:

```bash
pip install AMPY 
```

en la terminal, para utilizar la libreria verifique en que puerto esta conectado el ESP32.

- comando para ver docuemntos dentro de esp32:

```bash
ampy --port "puerto_esp32" ls
```

- comando para subir docuemntos dentro de esp32:

```bash
ampy --port "puerto_esp32" put "nombre_documento"
```

- comando para extraer docuemntos dentro de esp32:

```bash
ampy --port "puerto_esp32" get "nombre_documento"
```

- comando para correr docuemntos dentro de esp32:

```bash
ampy --port "puerto_esp32" run "nombre_documento"
```

## Avances

- Dia 18/12/2023:
  - Se hace lectura de datos de sensor de ulttrasonido.
  - Se genera archivo de texto el cual registra los datos obtenidos por el ESP32 a una frecuencia de 1Hz
  - Se crea conexion via wifi.
- Dia 19/12/2023:
  - Se crea server locar usando NODE.JS.
  - Se genera archivo CSV desde ESP32 y se hace escritura en el mismo.
  - Se genera primera peticion y respuesta conecntando ESP32 a server local usando protocolo http.
- Dia 20/12/2023
  - Se crea archivo de configuraciones para facilitar los cambios de variables globales.
  - Se pule todo el codigo evitando posible dexconexiones y facilitando la insercion de codigo de nuevos sensores. 

## Links

1. [Libreria Machine en Micropython](https://docs.micropython.org/en/latest/library/machine.html)
