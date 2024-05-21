from flask import Flask, request, jsonify

app - Flask(__name__)

@app.route('/', methods = ['POST'])
def receive_data():
    if request.is_json:
        data = request.get_json()
        temperature = data.get('temperature')
        humidity = data.get('dateTime')
        id = data.get('id')

        # mostrar valores no console
        print(f'Temperatura: {temperature}')
        print(f'Umidade: {humidity}')
        print(f'Horário: {dateTime}')
        print(f'Identificação: {id}')
