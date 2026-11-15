import psycopg2
from config import load_config

def get_connection():
    try:
        conn = psycopg2.connect(**load_config)
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None