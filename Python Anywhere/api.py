from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import google.generativeai as genai #pip install -q -U google-generativeai

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="AdrielFernando.mysql.pythonanywhere-services.com",
            user="AdrielFernando",
            password="adm12345",
            database="AdrielFernando$default"
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None
    

# def get_db_connection():
#     try:
#         conn = mysql.connector.connect(
#             host="ioshuan.mysql.pythonanywhere-services.com",
#             user="ioshuan",
#             password="p4$$w0rd",
#             database="ioshuan$db_iot"
#         )
#         return conn
#     except Error as e:
#         print(f"Error connecting to database: {e}")
#         return None



#configurações para o uso da API GEMINI

model = genai.GenerativeModel(model_name = "gemini-pro")
genai.configure(api_key = 'AIzaSyAciPbcn0--KEHuP_J78oE5t4U5IXPSmcU')


@app.route('/')
def index():
    try:
        conn = get_db_connection()
        if conn is not None:
            message = 'CONECTADO!'
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM log_acesso ORDER BY timestamp DESC LIMIT 1")
            result = mycursor.fetchone()
            mycursor.close()
            conn.close()

            if result:
                id, timestamp, evento, origem, temperature, humidity = result
            else:
                id, timestamp, evento, origem, temperature, humidity = None, None, None, None, None, None
                message = 'Nenhuma tupla encontrada.'
        else:
            id, timestamp, evento, origem, temperature, humidity = None, None, None, None, None, None
            message = 'NOT CONNECTED!'
    except Error as e:
        id, timestamp, evento, origem, temperature, humidity = None, None, None, None, None, None
        message = f'NOT CONNECTED! Error: {str(e)}'


#uso API GEMINI

    context_prompt = ["considere que voce é um especial horicultor ou agronomo, de acordo com valores recentes sobre temperatura, humidade , luminosidade de uma planta voce é capaz de geral uma análise geral e simples sobre o estado dessa planta"]

    prompt = [f"preciso que voce faça a análide da planta que está com esses valores - temperatura{temperature}, humidade{humidity}, a resposta deve conter até 35 palavras e sem caractetes especias como * ou barra / \ , deixe a resposta na mesma linha"]

    response = model.generate_content([context_prompt[0], prompt[0]])


    return render_template('index.html', message=message, id=id, timestamp=timestamp, evento=evento, origem=origem, temperature=temperature, humidity=humidity, analyticGemini=response.text)

@app.route('/post_data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        event = data['evento']
        origin = data['origem']
        temperature = data['temperature']
        humidity = data['humidity']

        # Obtendo a data e hora atuais
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO log_acesso (timestamp, evento, origem, temperature, humidity) VALUES (%s, %s, %s, %s, %s)", (timestamp, event, origin, temperature, humidity))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/received_data', methods=['GET'])
def show_received_data():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM log_acesso")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        data = [{"timestamp": row[0], "evento": row[1], "origem": row[2], "temperature": row[3], "humidity": row[4]} for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)


# curl -X POST https://AdrielFernando.pythonanywhere.com/post_data -H "Content-Type: application/json" -d "{\"evento\": \"Evento Teste\", \"origem\": \"Origem Teste\", \"temperature\": 23.5, \"humidity\": 60.2}"
