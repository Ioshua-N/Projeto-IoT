# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="ioshuan.mysql.pythonanywhere-services.com",
            user="ioshuan",
            password="p4$$w0rd",
            database="ioshuan$db_iot"
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

try:
    conn = get_db_connection()
    if conn is not None:
        message = 'CONNECTED!'
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM log_acesso")
        results = mycursor.fetchall()
        mycursor.close()
        conn.close()
    else:
        results = ["?"]
        message = 'NOT CONNECTED!'
except Error as e:
    results = ["?"]
    message = f'NOT CONNECTED! Error: {str(e)}'

@app.route('/')
def index():
    return render_template('index.html', message=message, results=results)

@app.route('/post_data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        timestamp = data['timestamp']
        event = data['evento']
        origin = data['origem']

        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO log_acesso (timestamp, evento, origem) VALUES (%s, %s, %s)", (timestamp, event, origin))
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

        data = [{"timestamp": row[0], "evento": row[1], "origem": row[2]} for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
