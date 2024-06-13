from models import CURSOR, CONN
from datetime import datetime

class CategoryManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def manage_categories(self):
        while True:
            print("\nCategories Management")
            print("1. View existing categories")
            print("2. Add Category")
            print("3. Delete Category")
            print("4. Edit Category Description")
            print("0. Back to Main Menu")
            
            choice = input("> ")
            if choice == "1":
                self.view_categories()
            elif choice == "2":
                self.add_category()
            elif choice == "3":
                self.delete_category()
            elif choice == "4":
                self.edit_category_description()
            elif choice == "0":
                break
            else:
                print("Invalid choice")

    def view_categories(self):
        CURSOR.execute("""
            SELECT 
                c.category_id, c.category_name, c.description, c.date_created, c.date_modified, GROUP_CONCAT(t.tag_name, ', ') AS tags
            FROM 
                category_table c
            LEFT JOIN 
                category_tag ct ON c.category_id = ct.category_id
            LEFT JOIN 
                tag_table t ON ct.tag_id = t.tag_id
            WHERE 
                c.created_by = ? OR c.created_by = 'predefined'
            GROUP BY 
                c.category_id, c.category_name, c.description, c.date_created, c.date_modified
        """, (self.user_id,))
        categories = CURSOR.fetchall()

        if categories:
            print("Existing Categories:")
            displayed_categories = set()
            for category in categories:
                category_id, category_name, description, date_created, date_modified, tags = category
                if category_name not in displayed_categories:
                    displayed_categories.add(category_name)
                    if tags:
                        print(f"{category_id}: {category_name} - {description} (Created: {date_created}, Modified: {date_modified}) [Tags: {tags}]")
                    else:
                        print(f"{category_id}: {category_name} - {description} (Created: {date_created}, Modified: {date_modified}) [No Tags]")
        else:
            print("No categories found.")

    def add_category(self):
        category_name = input("Enter category name: ")
        description = input("Enter category description: ")

        # Get tags for this category
        tags = input("Enter tags for this category")
        tag_ids = []
        for tag in tags:
            tag = tag.strip()
            if tag:
                CURSOR.execute("SELECT tag_id FROM tag_table WHERE tag_name = ?", (tag,))
                result = CURSOR.fetchone()
                if result:
                    tag_ids.append(result[0])
                else:
                    CURSOR.execute("INSERT INTO tag_table (tag_name) VALUES (?)", (tag,))
                    CONN.commit()
                    tag_ids.append(CURSOR.lastrowid)

        # Insert category into category_table
        CURSOR.execute("INSERT INTO category_table (category_name, description, created_by, date_created, date_modified) VALUES (?, ?, ?, ?, ?)", 
                       (category_name, description, self.user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        CONN.commit()
        category_id = CURSOR.lastrowid

        # Insert category-tag associations into category_tag table
        for tag_id in tag_ids:
            CURSOR.execute("INSERT INTO category_tag (category_id, tag_id) VALUES (?, ?)", (category_id, tag_id))
        CONN.commit()

        print(f"Category '{category_name}' added.")

    def delete_category(self):
        category_id = input("Enter category ID to delete: ")
        
        CURSOR.execute("DELETE FROM category_table WHERE category_id = ? AND created_by = ?", (category_id, self.user_id))
        CONN.commit()
        print(f"Category with ID '{category_id}' deleted.")

    def edit_category_description(self):
        category_id = input("Enter category ID to edit description: ")
        
        CURSOR.execute("SELECT * FROM category_table WHERE category_id = ?", (category_id,))
        category = CURSOR.fetchone()
        
        if category:
            if category[3] == 'predefined':
                print(f"Current description for {category[1]}: {category[2]}")
                print("Do you want to:")
                print("1. Replace the current description")
                print("2. Add the new description as another description")

                choice = input("> ")
                
                if choice == "1":
                    new_description = input("Enter new description: ")
                elif choice == "2":
                    new_description = category[2] + "\n" + input("Enter new description: ")
                else:
                    print("Invalid choice.")
                    return
                
                CURSOR.execute("UPDATE category_table SET description = ?, date_modified = ? WHERE category_id = ?", 
                               (new_description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), category_id))
                CONN.commit()
                print(f"Description for category '{category[1]}' updated.")
            else:
                print("You can only edit the description of a predefined category.")
        else:
            print("Category not found.")
