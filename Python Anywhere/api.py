from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def receive_data():
    try:
        data = request.get_json()
        temperature = data['temperature']
        humidity = data['humidity']

        print(f"Temperatura: {temperature}, Humidity: {humidity}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

#if __name__ == '__main__':
#    app.run(debug = True)

# testar o envio e recebimento local:
# curl -X POST https://ioshuan.pythonanywhere.com/ -H "Content-Type: application/json" -d "{\"temperature\": 25.0, \"humidity\": 60}"

# instalar as dependencias no python anywhere
# cd myapi
# pip install -r requirements.txt --user
