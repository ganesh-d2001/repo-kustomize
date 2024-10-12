from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging
import psycopg2
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Database connection details
DB_HOST = 'localhost'
DB_NAME = 'prod'
DB_USER = 'prod'
DB_PASSWORD = 'prod'
DB_PORT = '5432'

# Logging setup
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    filename=os.path.join(log_directory, 'backend.log'), 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def connect_to_db():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def create_people_table():
    """Create the people table if it does not exist."""
    try:
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS people (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    address TEXT,
                    interests TEXT
                );
                """
                cursor.execute(create_table_query)
                logging.info("Table 'people' checked/created successfully.")
    except Exception as e:
        logging.error(f'Error creating table: {str(e)}')

# Call this function when the app starts
create_people_table()

# Serve the index (cover page) HTML file
@app.route('/')
def serve_index():
    return render_template('index.html')

# Serve the people submission form page
@app.route('/Frontend.html')
def serve_submission():
    return render_template('Frontend.html')

# Serve the people data page
@app.route('/people_data.html')
def serve_people_data():
    return render_template('people_data.html')

# Serve the person detail page
@app.route('/person_detail.html')
def serve_person_detail():
    return render_template('person_detail.html')

# Endpoint to handle form submission (POST)
@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.json
        name = data.get('name')
        address = data.get('address')
        interests = data.get('interests')

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO people (name, address, interests) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (name, address, interests))
                logging.info(f'Data inserted: {name}, {address}, {interests}')

        return jsonify({"status": "success", "message": "Data inserted successfully!"}), 201
    except Exception as e:
        logging.error(f'Error inserting data: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 400

# Endpoint to fetch people data
@app.route('/people', methods=['GET'])
def fetch_people_data():
    try:
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name FROM people")
                people = cursor.fetchall()

        if not people:  # Check if the data is empty
            return jsonify({"status": "empty", "message": "No data available"}), 200

        people_list = [{"id": p[0], "name": p[1]} for p in people]
        return jsonify(people_list), 200
    except Exception as e:
        logging.error(f'Error fetching data: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/people/<int:person_id>', methods=['GET'])
def fetch_person_detail(person_id):
    try:
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, address, interests FROM people WHERE id = %s", (person_id,))
                person = cursor.fetchone()

        if not person:
            return jsonify({"status": "error", "message": "Person not found"}), 404

        person_detail = {
            "id": person[0],
            "name": person[1],
            "address": person[2],
            "interests": person[3]
        }
        return jsonify(person_detail), 200
    except Exception as e:
        logging.error(f'Error fetching person details: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
