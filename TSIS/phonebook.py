import json
import psycopg2
from config import load_config

def get_connection():
    try:
        return psycopg2.connect(**load_config)
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

def advanced_search():
    query = input("Введите текст для поиска (имя, email или часть телефона): ").strip()
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s);", (query,))
            rows = cur.fetchall()
            print(f"\n--- РЕЗУЛЬТАТЫ РАСШИРЕННОГО ПОИСКА ПО '{query}' ---")
            if not rows:
                print("Ничего не найдено.")
            for row in rows:
                print(f"ID: {row[0]} | Имя: {row[1]} | Email: {row[2]} | ДР: {row[3]} | Группа: {row[4]} | Тел: {row[5]} ({row[6]})")
        conn.close()

def add_new_phone():
    name = input("Введите имя существующего контакта: ").strip()
    phone = input("Введите номер телефона: ").strip()
    ptype = input("Введите тип телефона (home, work, mobile): ").strip().lower()
    
    if ptype not in ('home', 'work', 'mobile'):
        print("Ошибка: неверный тип телефона. Допустимо только: home, work, mobile.")
        return

    conn = get_connection()
    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, ptype))
            print("Телефон успешно добавлен!")
        except Exception as e:
            print(f"Ошибка при добавлении телефона: {e}")
        conn.close()

def assign_group():
    name = input("Введите имя контакта: ").strip()
    group = input("Введите название группы (Family, Work, Friend, Other и др.): ").strip()
    
    conn = get_connection()
    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("CALL move_to_group(%s, %s);", (name, group))
            print(f"Контакт '{name}' успешно перемещен в группу '{group}'!")
        except Exception as e:
            print(f"Ошибка: {e}")
        conn.close()

def paginated_navigation():
    try:
        limit = int(input("Записей на страницу (LIMIT): "))
    except ValueError:
        print("Введите число.")
        return

    offset = 0
    conn = get_connection()
    if not conn:
        return

    while True:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email, birthday FROM contacts ORDER BY id LIMIT %s OFFSET %s;", (limit, offset))
            rows = cur.fetchall()
            
            print(f"\n--- СТРАНИЦА (LIMIT {limit}, OFFSET {offset}) ---")
            if not rows:
                print("Больше нет записей.")
            for row in rows:
                print(f"ID: {row[0]} | Имя: {row[1]} | Email: {row[2]} | ДР: {row[3]}")

        action = input("\nКоманды: [n] следующий, [p] предыдущий, [q] выход в меню: ").strip().lower()
        if action == 'n':
            offset += limit
        elif action == 'p':
            offset = max(0, offset - limit)
        elif action == 'q':
            break
        else:
            print("Неизвестная команда.")
    conn.close()

def export_to_json():
    filename = input("Введите имя файла для экспорта (например, contacts.json): ").strip()
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.name, c.email, c.birthday, g.name 
                FROM contacts c LEFT JOIN groups g ON c.group_id = g.id;
            """)
            contacts = cur.fetchall()
            
            data = []
            for c in contacts:
                c_id, name, email, birthday, group = c
                cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s;", (c_id,))
                phones = [{"phone": p[0], "type": p[1]} for p in cur.fetchall()]
                
                data.append({
                    "name": name,
                    "email": email,
                    "birthday": str(birthday) if birthday else None,
                    "group": group,
                    "phones": phones
                })
                
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            print(f"Данные успешно экспортированы в {filename}!")
        conn.close()

def import_from_json():
    filename = input("Введите имя файла для импорта (например, contacts.json): ").strip()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return

    conn = get_connection()
    if not conn:
        return

    with conn:
        with conn.cursor() as cur:
            for item in data:
                name = item.get("name")
                email = item.get("email")
                birthday = item.get("birthday")
                group_name = item.get("group")
                phones = item.get("phones", [])

                # Проверяем, есть ли такой контакт
                cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
                existing = cur.fetchone()

                if existing:
                    choice = input(f"Контакт '{name}' уже существует. [s] пропустить / [o] перезаписать: ").strip().lower()
                    if choice == 's':
                        continue
                    elif choice == 'o':
                        cur.execute("UPDATE contacts SET email = %s, birthday = %s WHERE name = %s;", (email, birthday, name))
                        contact_id = existing[0]
                    else:
                        continue
                else:
                    group_id = None
                    if group_name:
                        cur.execute("INSERT INTO groups(name) VALUES(%s) ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name RETURNING id;", (group_name,))
                        res = cur.fetchone()
                        if res:
                            group_id = res[0]

                    cur.execute(
                        "INSERT INTO contacts(name, email, birthday, group_id) VALUES(%s, %s, %s, %s) RETURNING id;",
                        (name, email, birthday, group_id)
                    )
                    contact_id = cur.fetchone()[0]

                # Добавляем телефоны
                for p in phones:
                    cur.execute(
                        "INSERT INTO phones(contact_id, phone, type) VALUES(%s, %s, %s);",
                        (contact_id, p["phone"], p["type"])
                    )
    print("Импорт из JSON завершен!")
    conn.close()

def main():
    while True:
        print("\n=== PHONEBOOK APPLICATION (Practice 9) ===")
        print("1. Расширенный поиск (по имени, email, телефонам)")
        print("2. Добавить телефон к контакту (add_phone)")
        print("3. Переместить контакт в группу (move_to_group)")
        print("4. Интерактивная пагинация (next / prev)")
        print("5. Экспорт в JSON")
        print("6. Импорт из JSON")
        print("0. Выход")
        
        choice = input("Выбери пункт меню (0-6): ").strip()
        
        if choice == '1':
            advanced_search()
        elif choice == '2':
            add_new_phone()
        elif choice == '3':
            assign_group()
        elif choice == '4':
            paginated_navigation()
        elif choice == '5':
            export_to_json()
        elif choice == '6':
            import_from_json()
        elif choice == '0':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор, попробуй снова.")

if __name__ == "__main__":
    main()