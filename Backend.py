import logging
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Configure logging to log to a file
logging.basicConfig(filename='/app/logs/backend.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection parameters
DB_HOST = 'localhost'  # or your Cloud SQL instance IP
DB_NAME = 'prod'
DB_USER = 'prod'
DB_PASSWORD = 'prod'
DB_PORT = '5432'

# Function to connect to PostgreSQL
def connect_to_db():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return connection

# Function to create the table if it doesn't exist
def create_table():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            address VARCHAR(255),
            interests TEXT
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()
    logging.info('Table created or already exists.')

# Endpoint to handle form submission (POST)
@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.json
        name = data.get('name')
        address = data.get('address')
        interests = data.get('interests')
        print(f"Incoming data: {data}")

        connection = connect_to_db()
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO people (name, address, interests)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (name, address, interests))
        connection.commit()

        cursor.close()
        connection.close()

        logging.info(f'Data inserted: {name}, {address}, {interests}')
        return jsonify({"status": "success", "message": "Data inserted successfully!"}), 201
    except Exception as e:
        logging.error(f'Error inserting data: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    create_table()
    logging.info('Starting Flask application...')
    app.run(host='0.0.0.0', port=5000)
