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

        return jsonify({"message": "Dados recebidos com sucesso"}), 200
    else:
        return jsonify({"error": "Formato JSON errado"}), 400

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8888)
