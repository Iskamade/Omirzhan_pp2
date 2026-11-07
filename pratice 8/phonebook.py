import psycopg2
from config import load_config

def get_connection():
    try:
        return psycopg2.connect(**load_config)
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

def search_pattern():
    pattern = input("Введите текст для поиска (имя или часть телефона): ").strip()
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            # Функции вызываются через SELECT
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
            rows = cur.fetchall()
            print(f"\n--- РЕЗУЛЬТАТЫ ПОИСКА ПО ПАТТЕРНУ '{pattern}' ---")
            for row in rows:
                print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
        conn.close()

def upsert_user():
    name = input("Введите имя контакта: ").strip()
    phone = input("Введите телефон: ").strip()
    conn = get_connection()
    if conn:
        with conn:
            with conn.cursor() as cur:
                # Процедуры вызываются через CALL
                cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
        print("Контакт успешно добавлен / обновлен (Upsert)!")
        conn.close()

def paginated_view():
    try:
        limit = int(input("Сколько записей выводить на страницу (LIMIT)?: "))
        offset = int(input("Сколько записей пропустить (OFFSET)?: "))
    except ValueError:
        print("Ошибка: введите числа.")
        return

    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
            rows = cur.fetchall()
            print(f"\n--- СТРАНИЦА КОНТАКТОВ (LIMIT {limit}, OFFSET {offset}) ---")
            for row in rows:
                print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
        conn.close()

def delete_user():
    query = input("Введите имя или телефон контакта для удаления: ").strip()
    conn = get_connection()
    if conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s);", (query,))
        print("Процедура удаления выполнена.")
        conn.close()

def main():
    while True:
        print("\n=== PHONEBOOK APPLICATION (Practice 8) ===")
        print("1. Поиск по паттерну (Функция)")
        print("2. Добавить / Обновить контакт - Upsert (Процедура)")
        print("3. Просмотр с пагинацией (Функция)")
        print("4. Удалить контакт (Процедура)")
        print("0. Выход")
        
        choice = input("Выбери пункт меню (0-4): ").strip()
        
        if choice == '1':
            search_pattern()
        elif choice == '2':
            upsert_user()
        elif choice == '3':
            paginated_view()
        elif choice == '4':
            delete_user()
        elif choice == '0':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор, попробуй снова.")

if __name__ == "__main__":
    main()