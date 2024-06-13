from datetime import datetime                                           
from models import CONN, CURSOR, initialize_db
from categories import CategoryManager
from entries import EntryManager
from tags import TagManager

def get_connection():
    return CONN

def login_or_signup():
    print("WELCOME TO 'JOURNAL AWAY'!")
    while True:
        user_choice = input("Are you a new user? (yes/no): ").strip().lower()
        if user_choice == 'yes':
            return sign_up()
        elif user_choice == 'no':
            return log_in()
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

def sign_up():
    print("SIGN UP")
    while True:
        username = input("Create your username: ").strip()
        
        while True:
            user_id = input("Create your user ID: ").strip()
            CURSOR.execute("SELECT * FROM user_table WHERE user_id = ?", (user_id,))
            existing_user = CURSOR.fetchone()
            
            if existing_user:
                print("User ID already exists. Please choose a different one.")
            else:
                break

        date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        CURSOR.execute("INSERT INTO user_table (user_id, username, date_joined) VALUES (?, ?, ?)", 
                       (user_id, username, date_joined))
        CONN.commit()
        
        print(f"User {username} with ID {user_id} has been created.")
        return user_id


def log_in():
    print("LOG IN")
    while True:
        username = input("Enter your username: ")
        user_id = input("Enter your user ID: ")

        CURSOR.execute("SELECT * FROM user_table WHERE user_id = ? AND username = ?", (user_id, username))
        user = CURSOR.fetchone()

        if user:
            print(f"WELCOME BACK, {username}!")
            return user_id
        else:
            print("Invalid username or user ID. Please try again.")

def exit_program():
    print("Goodbye! See you next time.")
    CONN.close()
    exit()

def main():
    initialize_db()
    user_id = login_or_signup()
    
    while True:
        print("\nMain Menu")
        print("1. Manage Categories")
        print("2. Manage Entries")
        print("3. Manage Tags")
        print("0. Exit")
        
        choice = input("> ")
        if choice == "1":
            manager = CategoryManager(user_id)
            manager.manage_categories()
        elif choice == "2":
            manager = EntryManager(user_id)
            manager.manage_entries()
        elif choice == "3":
            manager = TagManager(user_id)
            manager.manage_tags()
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()

