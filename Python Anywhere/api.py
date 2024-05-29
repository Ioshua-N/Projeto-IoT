from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

received_data = []


# conexão com o banco de dados !!!!!!!

db_config = {
    'user': 'AdrielFernando',
    'password': 'adm12345',
    'host': 'AdrielFernando.mysql.pythonanywhere-services.com',
    'database': 'AdrielFernando$default'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# conexão com o banco de dados !!!!!!!!!


@app.route('/', methods = ['POST'])
def receive_data():
    try:
        data = request.get_json()
        temperature = data['temperature']
        humidity = data['humidity']


        # Salvar dados no banco de dados!!!!!!!!

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dados (temperature, humidity) VALUES (%s, %s)", (temperature, humidity))
        conn.commit()
        cursor.close()
        conn.close()

         # Salvar dados no banco de dados!!!!!!!!

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

# curl -X POST https://adrielfernando.pythonanywhere.com/ -H "Content-Type: application/json" -d "{\"temperature\": 25.0, \"humidity\": 60}"

# instalar as dependencias no python anywhere
# cd myapi
# pip install -r requirements.txt --user
