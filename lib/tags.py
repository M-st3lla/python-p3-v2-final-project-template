from models import CURSOR, CONN

class TagManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def manage_tags(self):
        while True:
            print("\nTags Management")
            print("1. View Existing Tags")
            print("2. Delete Tag")
            print("0. Back to Main Menu")
            
            choice = input("> ")
            if choice == "1":
                self.view_tags()
            elif choice == "2":
                self.delete_tag()
            elif choice == "0":
                break
            else:
                print("Invalid choice")

    def view_tags(self):
        CURSOR.execute("SELECT tag_id, tag_name, description FROM tag_table")
        tag_rows = CURSOR.fetchall()
        
        if tag_rows:
            print("Existing Tags:")
            for tag in tag_rows:
                print(f"{tag[0]}: {tag[1]} - {tag[2]}")
        else:
            print("No tags found.")

    def delete_tag(self):
        tag_id = input("Enter tag ID to delete: ")
        
        CURSOR.execute("DELETE FROM tag_table WHERE tag_id = ?", (tag_id,))
        CONN.commit()
        print(f"Tag with ID '{tag_id}' deleted.")
