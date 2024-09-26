import psycopg2

# Database connection parameters
DB_HOST = 'localhost'
DB_NAME = 'your_database_name'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_PORT = '5432'  # default PostgreSQL port

# Function to connect to PostgreSQL
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        print("Connected to the database")
        return connection
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None

# Function to create the table if it doesn't exist
def create_table():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS people (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                address VARCHAR(255),
                interests TEXT
            );
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("Table 'people' created or already exists.")
            cursor.close()
        except Exception as error:
            print(f"Failed to create table: {error}")
        finally:
            connection.close()

# Function to insert an entry into the table
def insert_person(name, address, interests):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO people (name, address, interests)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (name, address, interests))
            connection.commit()
            print(f"Inserted {name} into the database.")
            cursor.close()
        except Exception as error:
            print(f"Failed to insert data: {error}")
        finally:
            connection.close()

# Sample data to be inserted
people_data = [
    ('Alice', '123 Main St', 'Reading, Hiking'),
    ('Bob', '456 Oak Ave', 'Music, Cooking'),
    ('Charlie', '789 Pine Dr', 'Traveling, Coding')
]

# Main execution
if __name__ == '__main__':
    # Step 1: Create table
    create_table()

    # Step 2: Insert data into the table
    for person in people_data:
        insert_person(person[0], person[1], person[2])
