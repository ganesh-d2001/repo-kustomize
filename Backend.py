from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging
import psycopg2
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, static_folder='static', template_folder='templates')
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)
CORS(app)

# Fetch database connection details from environment variables
DB_HOST = os.getenv('DB_HOST', 'postgresql-db-service-test')
DB_USER = os.getenv('DB_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'Test@123')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')

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
        user=DB_USER,
        password=POSTGRES_PASSWORD,
        dbname=DB_NAME,
        port=DB_PORT
    )
def create_prod_database():
    """Create the prod database if it does not exist."""
    try:
        # Connect to the default postgres database to create the prod database
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Check if the database exists
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'prod'")
                result = cursor.fetchone()
                
                if result is None:
                    # Database doesn't exist, create it
                    cursor.execute("CREATE DATABASE prod")
                    logging.info("Database 'prod' created successfully.")
                else:
                    logging.info("Database 'prod' already exists.")
    except Exception as e:
        logging.error(f'Error creating database: {str(e)}')

create_prod_database()

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

# Serve the index (cover page) HTML file at /app
# Serve the index (cover page) HTML file at /
@app.route('/')
def serve_index():
    return render_template('index.html')

# Serve the people submission form page at /app/Frontend.html
@app.route('/Frontend.html')
def serve_submission():
    return render_template('Frontend.html')

# Serve the people data page at /app/people_data.html
@app.route('/people_data.html')
def serve_people_data():
    return render_template('people_data.html')

# Serve the person detail page at /app/person_detail.html
@app.route('/person_detail.html')
def serve_person_detail():
    return render_template('person_detail.html')

# Endpoint to handle form submission (POST) at /app/submit
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

# Endpoint to fetch people data at /app/people
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

# Fetch a person's detail at /app/people/<int:person_id>
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

# Search for a person by name at /app/people/search
@app.route('/people/search', methods=['GET'])
def search_people_by_name():
    name = request.args.get('name')
    try:
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                search_query = "SELECT id, name, address, interests FROM people WHERE name ILIKE %s"
                cursor.execute(search_query, (f'%{name}%',))
                person = cursor.fetchone()

        if person:
            return jsonify({"id": person[0], "name": person[1], "address": person[2], "interests": person[3]})
        else:
            return jsonify({"status": "error", "message": "Person not found"}), 404
    except Exception as e:
        logging.error(f'Error searching for person: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500
    #

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
