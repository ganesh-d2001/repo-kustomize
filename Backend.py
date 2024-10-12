from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import logging
import psycopg2
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Database connection details
DB_HOST = 'localhost'
DB_NAME = 'prod'
DB_USER = 'prod'
DB_PASSWORD = 'prod'
DB_PORT = '5432'

# Logging setup
logging.basicConfig(filename='/app/logs/backend.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_db():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return connection

# Serve the index (cover page) HTML file
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve the people submission form page
@app.route('/data_submission.html')
def serve_submission():
    return send_from_directory(app.static_folder, 'data_submission.html')

# Serve the people data page
@app.route('/people_data.html')
def serve_people_data():
    return send_from_directory(app.static_folder, 'people_data.html')

# Endpoint to handle form submission (POST)
@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.json
        name = data.get('name')
        address = data.get('address')
        interests = data.get('interests')

        connection = connect_to_db()
        cursor = connection.cursor()
        insert_query = "INSERT INTO people (name, address, interests) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, address, interests))
        connection.commit()

        cursor.close()
        connection.close()

        logging.info(f'Data inserted: {name}, {address}, {interests}')
        return jsonify({"status": "success", "message": "Data inserted successfully!"}), 201
    except Exception as e:
        logging.error(f'Error inserting data: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 400

# Endpoint to fetch people data
@app.route('/people', methods=['GET'])
def fetch_people_data():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM people")
        people = cursor.fetchall()

        cursor.close()
        connection.close()

        people_list = [{"id": p[0], "name": p[1]} for p in people]
        return jsonify(people_list), 200
    except Exception as e:
        logging.error(f'Error fetching data: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
