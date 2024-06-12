from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Importe o CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Adicione o CORS à sua aplicação Flask

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Configurações para o uso da API GEMINI
model = genai.GenerativeModel(model_name="gemini-pro")
genai.configure(api_key=os.getenv('GENAI_API_KEY'))

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
                id, timestamp, evento, origem, temperature, humidity, luz = result
                # Uso da API GEMINI
                context_prompt = ["considere que voce é um especial horicultor ou agronomo, de acordo com valores recentes sobre temperatura, humidade , luminosidade de uma planta voce é capaz de geral uma análise geral e simples sobre o estado dessa planta"]
                prompt = [f"preciso que voce faça a análise da planta que está com esses valores - temperatura{temperature}, humidade{humidity}, luminosidade{luz} - a resposta deve conter até 35 palavras e sem caractetes especias como * ou barra / \ , deixe a resposta na mesma linha"]
                response = (model.generate_content([context_prompt[0], prompt[0]])).text
                # Integração dos valores e da resposta em uma única string
                response = f"Humor: {response}, Temperatura: {temperature}, Umidade: {humidity}, Luminosidade: {luz}"
            else:
                response = 'Nenhuma tupla encontrada.'
        else:
            response = 'NOT CONNECTED!'
    except Error as e:
        response = f'NOT CONNECTED! Error: {str(e)}'

    return response  # Retornando a resposta contendo a análise e os valores de temperatura, umidade e luminosidade

@app.route('/post_data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        event = data['evento']
        origin = data['origem']
        temperature = data['temperature']
        humidity = data['humidity']
        luz = data['light']

        # Obtendo a data e hora atuais
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO log_acesso (timestamp, evento, origem, temperature, humidity, luz) VALUES (%s, %s, %s, %s, %s, %s)", (timestamp, event, origin, temperature, humidity, luz))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400



@app.route('/analyticGemini')
def analytic():
    luz_list = []
    humidity_list = []
    temperature_list = []
    message = ''
    try:
        conn = get_db_connection()
        if conn is not None:
            message = 'CONECTADO!'
            mycursor = conn.cursor()
            
            # Consulta para pegar os últimos 10 valores das colunas "luz", "humidity" e "temperature"
            
            mycursor.execute("SELECT luz FROM log_acesso ORDER BY timestamp DESC LIMIT 10")
            luz_values = mycursor.fetchall()
            luz_list = [row[0] for row in luz_values]
    
            mycursor.execute("SELECT humidity FROM log_acesso ORDER BY timestamp DESC LIMIT 10")
            humidity_values = mycursor.fetchall()
            humidity_list = [row[0] for row in humidity_values]
    
            mycursor.execute("SELECT temperature FROM log_acesso ORDER BY timestamp DESC LIMIT 10")
            temperature_values = mycursor.fetchall()
            temperature_list = [row[0] for row in temperature_values]
    
            # Fechar o cursor e a conexão
            mycursor.close()
            conn.close()
    
            # Para o restante do código
            conn = get_db_connection()
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM log_acesso ORDER BY timestamp DESC LIMIT 1")
            result = mycursor.fetchone()
            mycursor.close()
            conn.close()
    
            if result:
                id, timestamp, evento, origem, temperature, humidity, luz = result
            else:
                id, timestamp, evento, origem, temperature, humidity, luz = None, None, None, None, None, None, None
                message = 'Nenhuma tupla encontrada.'
        else:
            id, timestamp, evento, origem, temperature, humidity, luz = None, None, None, None, None, None, None
            message = 'NOT CONNECTED!'
    except Error as e:
        id, timestamp, evento, origem, temperature, humidity, luz = None, None, None, None, None, None, None
        message = f'NOT CONNECTED! Error: {str(e)}'

    

    # Uso da API GEMINI
    promptTemperature = ["considere que voce é um especial horicultor ou agronomo, de acordo com valores recentes sobre temperatura, humidade , luminosidade de uma planta que não esses - {temperature_list}  forcena uma analise apenas sobre esse aspecto da planta, forneça recomendações de como melhorar, é muito importante deixar tudo na mesma linha e não coloque nenhum caracter especial como * e // "]

    promptHumidity = ["considere que voce é um especial horicultor ou agronomo, de acordo com valores recentes sobre humidade de uma planta que não esses - {humidity_list} forcena uma analise apenas sobre esse aspecto da planta, forneça recomendações de como melhorar, é muito importante deixar tudo na mesma linha e não coloque nenhum caracter especial como * e // "]

    promptLuz = ["considere que voce é um especial horicultor ou agronomo, de acordo com valores recentes sobre a luminosidade de uma planta que não esses - {luz_list} forcena uma analise apenas sobre esse aspecto da planta, forneça recomendações de como melhorar, é muito importante deixar tudo na mesma linha e não coloque nenhum caracter especial como * e // "]

    responseTemperature = (model.generate_content(promptTemperature[0])).text

    responseHumidity = model.generate_content(promptHumidity[0]).text

    responseLuz = (model.generate_content(promptLuz[0])).text

    # responseTemperature, responseHumidity, responseLuz, message = create_prompts()
    
    if message == 'CONECTADO!':
        print(responseTemperature)
        print(responseHumidity)
        print(responseLuz)
    else:
        print(message)
        
    # return responseTemperature, responseHumidity, responseLuz

    return {
    "temperature": responseTemperature,
    "humidity": responseHumidity,
    "luz": responseLuz
    }


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

        data = [{"timestamp": row[0], "evento": row[1], "origem": row[2], "temperature": row[3], "humidity": row[4], "luz": row[5]} for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(port=8002)
