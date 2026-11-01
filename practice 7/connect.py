import psycopg2
from config import load_config

def get_connection():
    try:
        connection = psycopg2.connect(**load_config)
        return connection
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Database connection error: {error}")
        return None

def create_tables():
    command = """
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            phone VARCHAR(50) NOT NULL UNIQUE
        )
    """
    conn = get_connection()
    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(command)
            print("Table is ready to use!")
        except Exception as error:
            print(f"Error creating table: {error}")
        finally:
            conn.close()

if __name__ == '__main__':
    create_tables()