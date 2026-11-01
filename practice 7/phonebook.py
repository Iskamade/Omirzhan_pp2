import csv
import psycopg2
from connect import get_connection, create_tables

def add_contact_console():
    name = input("Enter name (e.g., Dino, Siko, Sikosavr, Serik): ").strip()
    phone = input("Enter phone number: ").strip()

    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
                    (name, phone)
                )
        print(f"Contact '{name}' successfully added!")
    except psycopg2.IntegrityError:
        print("Error: A contact with this phone number already exists.")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        conn.close()

def import_from_csv(filename="contacts.csv"):
    conn = get_connection()
    if not conn:
        return
    
    count = 0
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            with conn:
                with conn.cursor() as cur:
                    for row in reader:
                        name = row['first_name'].strip()
                        phone = row['phone'].strip()
                        try:
                            cur.execute(
                                "INSERT INTO contacts (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                                (name, phone)
                            )
                            count += 1
                        except Exception:
                            pass
        print(f"Import completed! Added entries from file: {count}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as error:
        print(f"Error during import: {error}")
    finally:
        conn.close()

def update_contact():
    search_val = input("Enter name (e.g., Sikosavr) or phone to search: ").strip()

    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, first_name, phone FROM contacts WHERE first_name ILIKE %s OR phone ILIKE %s",
                (f"%{search_val}%", f"%{search_val}%")
            )
            rows = cur.fetchall()

            if not rows:
                print("No contacts found.")
                return

            print("\nFound contacts:")
            for idx, row in enumerate(rows):
                print(f"{idx + 1}. {row[1]} — {row[2]}")

            choice = input("Select contact number to edit (0 to cancel): ").strip()
            if not choice.isdigit() or int(choice) == 0:
                return
            
            selected_idx = int(choice) - 1
            if selected_idx < 0 or selected_idx >= len(rows):
                print("Invalid choice.")
                return
            
            contact_id = rows[selected_idx][0]

            print("\nWhat do you want to update?")
            print("1. Name")
            print("2. Phone")
            print("3. Both Name and Phone")
            sub_choice = input("Choice (1-3): ").strip()

            with conn:
                if sub_choice == '1':
                    new_name = input("New name: ").strip()
                    cur.execute("UPDATE contacts SET first_name = %s WHERE id = %s", (new_name, contact_id))
                    print("Name updated!")
                elif sub_choice == '2':
                    new_phone = input("New phone: ").strip()
                    cur.execute("UPDATE contacts SET phone = %s WHERE id = %s", (new_phone, contact_id))
                    print("Phone updated!")
                elif sub_choice == '3':
                    new_name = input("New name: ").strip()
                    new_phone = input("New phone: ").strip()
                    cur.execute("UPDATE contacts SET first_name = %s, phone = %s WHERE id = %s", (new_name, new_phone, contact_id))
                    print("Contact fully updated!")
    except Exception as error:
        print(f"Error during update: {error}")
    finally:
        conn.close()

def query_contacts():
    print("\n--- Search Contacts ---")
    print("1. Show all (Dino, Siko, Sikosavr, Serik...)")
    print("2. Search by name")
    print("3. Search by phone prefix")
    choice = input("Choice (1-3): ").strip()

    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            if choice == '1':
                cur.execute("SELECT first_name, phone FROM contacts ORDER BY first_name")
            elif choice == '2':
                name_query = input("Enter name or part of name: ").strip()
                cur.execute("SELECT first_name, phone FROM contacts WHERE first_name ILIKE %s", (f"%{name_query}%",))
            elif choice == '3':
                prefix = input("Enter phone prefix (e.g., +7701): ").strip()
                cur.execute("SELECT first_name, phone FROM contacts WHERE phone LIKE %s", (f"{prefix}%",))
            else:
                print("Invalid choice.")
                return

            rows = cur.fetchall()
            if not rows:
                print("No results.")
            else:
                print(f"\nContacts found: {len(rows)}")
                print("-" * 30)
                for name, phone in rows:
                    print(f"• {name} — {phone}")
                print("-" * 30)
    except Exception as error:
        print(f"Search error: {error}")
    finally:
        conn.close()

def delete_contact():
    identifier = input("Enter name or phone to delete: ").strip()

    conn = get_connection()
    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, first_name, phone FROM contacts WHERE first_name ILIKE %s OR phone = %s", (identifier, identifier))
                rows = cur.fetchall()

                if not rows:
                    print("Contact not found.")
                    return
                
                if len(rows) > 1:
                    print("Multiple matches found:")
                    for idx, row in enumerate(rows):
                        print(f"{idx + 1}. {row[1]} — {row[2]}")
                    choice = input("Select contact number to delete (0 to cancel): ").strip()
                    if not choice.isdigit() or int(choice) == 0:
                        return
                    selected_idx = int(choice) - 1
                    contact_id = rows[selected_idx][0]
                else:
                    contact_id = rows[0][0]

                cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
                print("Contact successfully deleted!")
    except Exception as error:
        print(f"Delete error: {error}")
    finally:
        conn.close()

def main():
    create_tables()

    while True:
        print("\n=== PHONEBOOK APPLICATION ===")
        print("1. Add contact")
        print("2. Import from contacts.csv")
        print("3. Update contact")
        print("4. Search / View contacts")
        print("5. Delete contact")
        print("0. Exit")
        
        choice = input("Select an option (0-5): ").strip()

        if choice == '1':
            add_contact_console()
        elif choice == '2':
            import_from_csv()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Please enter a number between 0 and 5.")

if __name__ == "__main__":
    main()