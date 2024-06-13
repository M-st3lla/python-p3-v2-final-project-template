from models import CURSOR, CONN
from datetime import datetime

class EntryManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def manage_entries(self):
        while True:
            print("\nEntries Management")
            print("1. View Existing Entries")
            print("2. Add New Entry")
            print("3. Delete Entry")
            print("0. Back to Main Menu")
            
            choice = input("> ")
            if choice == "1":
                self.view_entries()
            elif choice == "2":
                self.add_entry()
            elif choice == "3":
                self.delete_entry()
            elif choice == "0":
                break
            else:
                print("Invalid choice")

    def view_entries(self):
        CURSOR.execute("SELECT * FROM entry_table WHERE created_by = ?", (self.user_id,))
        entries = CURSOR.fetchall()
        
        if entries:
            print("Existing Entries:")
            for entry in entries:
                entry_id, entry_name, description, created_by, date_created = entry
                print(f"{entry_id}: {entry_name} - {description} (Created on: {date_created})")
        else:
            print("No entries found.")

    def add_entry(self):
        entry_name = input("Enter entry name: ")
        description = input("Enter entry description: ")
        
        CURSOR.execute("INSERT INTO entry_table (entry_name, description, created_by, date_created) VALUES (?, ?, ?, datetime('now'))", 
                       (entry_name, description, self.user_id))
        CONN.commit()
        print(f"Entry '{entry_name}' added.")

        entry_id = CURSOR.lastrowid
        tags = input("Enter tags for this entry: ")
        for tag in tags:
            tag = tag.strip()
            if tag:
                CURSOR.execute("SELECT tag_id FROM tag_table WHERE tag_name = ?", (tag,))
                result = CURSOR.fetchone()
                if result:
                    CURSOR.execute("INSERT INTO entry_tag (entry_id, tag_id) VALUES (?, ?)", (entry_id, result[0]))
                else:
                    print(f"Tag '{tag}' not found. Skipping.")
        CONN.commit()
        print("Entry added successfully.")

    def delete_entry(self):
        entry_id = input("Enter entry ID to delete: ")
        
        CURSOR.execute("DELETE FROM entry_table WHERE entry_id = ? AND created_by = ?", (entry_id, self.user_id))
        CONN.commit()
        print(f"Entry with ID '{entry_id}' deleted.")
