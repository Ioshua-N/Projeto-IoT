from flask import Flask, request, jsonify

app = Flask(__name__)

received_data = []

@app.route('/', methods = ['POST'])
def receive_data():
    try:
        data = request.get_json()
        temperature = data['temperature']
        humidity = data['humidity']

        received_data.append(data)

        print(f"Temperatura: {temperature}, Humidity: {humidity}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    
@app.route('/received_data', methods=['GET'])
def show_received_data():
    return jsonify(received_data)


#if __name__ == '__main__':
#    app.run(debug = True)

# testar o envio e recebimento local:
# curl -X POST https://ioshuan.pythonanywhere.com/ -H "Content-Type: application/json" -d "{\"temperature\": 25.0, \"humidity\": 60}"

# curl -X POST https://adrielfernando.pythonanywhere.com/ -H "Content-Type: application/json" -d "{\"temperature\": 25.0, \"humidity\": 24}"

#testar a método GET :

#curl -X POST https://adrielfernando.pythonanywhere.com/ -H "Content-Type: application/json" -d "{\"temperature\": 25.0, \"humidity\": 61}"

# instalar as dependencias no python anywhere
# cd myapi
# pip install -r requirements.txt --user
