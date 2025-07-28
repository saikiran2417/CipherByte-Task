import re
import json
import datetime
import os
import sys

CONTACTS_FILE = "contacts.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(contacts, file, indent=4)

def print_boxed_title(title):
    print("\n" + "=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)

def display_menu():
    print_boxed_title("ContactMaster - Main Menu")
    print("1. ➕ Add New Contact")
    print("2. ✏️ Edit Contact")
    print("3. ❌ Delete Contact")
    print("4. 🔍 Search Contact")
    print("5. 📒 View All Contacts")
    print("6. 🗑️ Clear All Contacts")
    print("7. 🚪 Exit")
    print("=" * 60)

def validate_input(prompt, pattern, error_msg):
    while True:
        value = input(prompt).strip()
        if re.fullmatch(pattern, value):
            return value
        print(f"⚠️ {error_msg}")

def validate_name():
    return validate_input(
        "Enter contact name (letters & spaces only): ",
        r"[A-Za-z ]{2,50}",
        "Invalid name! Only letters and spaces allowed (2–50 characters)."
    )

def validate_phone():
    return validate_input(
        "Enter 10-digit phone number: ",
        r"\d{10}",
        "Invalid phone number! Enter exactly 10 digits."
    )

def validate_email():
    return validate_input(
        "Enter email address (e.g., name@example.com): ",
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "Invalid email format! Please follow name@example.com format."
    )

def find_contact(contacts, search_term):
    return [c for c in contacts if search_term.lower() in c['name'].lower() 
            or search_term in c['phone'] 
            or search_term.lower() in c['email'].lower()]

def select_contact(results):
    for idx, contact in enumerate(results, 1):
        print(f"{idx}. {contact['name']} | 📞 {contact['phone']} | 📧 {contact['email']}")
    try:
        choice = int(input("Select contact number: ")) - 1
        if 0 <= choice < len(results):
            return choice
    except ValueError:
        pass
    print("⚠️ Invalid selection.")
    return None

def add_contact(contacts):
    print_boxed_title("Add New Contact")
    name = validate_name()
    phone = validate_phone()
    email = validate_email()

    if any(c for c in contacts if c['phone'] == phone or c['email'].lower() == email.lower()):
        print("⚠️ Contact with this phone/email already exists!")
        return

    contact = {
        'name': name,
        'phone': phone,
        'email': email,
        'added': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    contacts.append(contact)
    save_contacts(contacts)
    print(f"\n✅ Contact for '{name}' added successfully!")

def edit_contact(contacts):
    print_boxed_title("Edit Contact")
    search_term = input("Enter name/phone/email to edit: ").strip()
    results = find_contact(contacts, search_term)

    if results:
        choice = select_contact(results)
        if choice is not None:
            contact = results[choice]
            print(f"\nEditing contact: {contact['name']}")
            contact['name'] = validate_name()
            contact['phone'] = validate_phone()
            contact['email'] = validate_email()
            contact['added'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_contacts(contacts)
            print("✅ Contact updated successfully!")
    else:
        print("🚫 No matching contacts found.")

def delete_contact(contacts):
    print_boxed_title("Delete Contact")
    search_term = input("Enter name/phone/email to delete: ").strip()
    results = find_contact(contacts, search_term)

    if results:
        choice = select_contact(results)
        if choice is not None:
            confirm = input(f"Are you sure you want to delete '{results[choice]['name']}'? (yes/no): ").strip().lower()
            if confirm == 'yes':
                contacts.remove(results[choice])
                save_contacts(contacts)
                print("🗑️ Contact deleted successfully.")
            else:
                print("❌ Deletion canceled.")
    else:
        print("🚫 No matching contacts found.")

def search_contact(contacts):
    print_boxed_title("Search Contact")
    keyword = input("Enter name/phone/email to search: ").strip()
    results = find_contact(contacts, keyword)

    if results:
        print("\n🔎 Matching Contacts:")
        for idx, c in enumerate(results, 1):
            print(f"{idx}. {c['name']} | 📞 {c['phone']} | 📧 {c['email']} | 🕒 Added: {c['added']}")
    else:
        print("🚫 No matching contacts found.")

def view_all_contacts(contacts):
    print_boxed_title("All Contacts")
    if contacts:
        sorted_contacts = sorted(contacts, key=lambda x: x['name'].lower())
        for idx, c in enumerate(sorted_contacts, 1):
            print(f"{idx}. {c['name']} | 📞 {c['phone']} | 📧 {c['email']} | 🕒 Added: {c['added']}")
        print(f"\n📇 Total contacts: {len(contacts)}")
    else:
        print("📭 No contacts found.")

def clear_all_contacts(contacts):
    print_boxed_title("Clear All Contacts")
    confirm = input("⚠️ Are you sure you want to delete ALL contacts? (yes/no): ").strip().lower()
    if confirm == 'yes':
        contacts.clear()
        save_contacts(contacts)
        print("🗑️ All contacts deleted successfully.")
    else:
        print("❌ Clear operation canceled.")

def main():
    contacts = load_contacts()
    while True:
        display_menu()
        choice = input("Select an option (1-7): ").strip()
        clear_screen()

        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            edit_contact(contacts)
        elif choice == '3':
            delete_contact(contacts)
        elif choice == '4':
            search_contact(contacts)
        elif choice == '5':
            view_all_contacts(contacts)
        elif choice == '6':
            clear_all_contacts(contacts)
        elif choice == '7':
            print("\n👋 Exiting ContactMaster. Have a great day!")
            break
        else:
            print("❌ Invalid option. Please choose from 1 to 7.")

        input("\nPress Enter to return to the main menu...")
        clear_screen()

if __name__ == "__main__":
    main()