import sqlite3

class StockItem:
    def __init__(self, name, sku, quantity, price):
        self.name = name
        self.sku = sku
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"Name: {self.name}, SKU: {self.sku}, Quantity: {self.quantity}, Price: ${self.price:.2f}"

class InventoryManagement:
    def __init__(self, db_name="inventory.db"):
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                sku TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def add_item(self, name, sku, quantity, price):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO stock (sku, name, quantity, price) VALUES (?, ?, ?, ?)",
                (sku, name, quantity, price)
            )
            conn.commit()
            print("Item added successfully.")
        except sqlite3.IntegrityError:
            print(f"Error: An item with SKU '{sku}' already exists.")
        finally:
            conn.close()

    def view_stock(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT sku, name, quantity, price FROM stock")
        rows = cursor.fetchall()
        conn.close()

        if rows:
            for sku, name, quantity, price in rows:
                item = StockItem(name, sku, quantity, price)
                print(item)
        else:
            print("No items in stock.")

    def remove_item(self, sku):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stock WHERE sku = ?", (sku,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Item with SKU '{sku}' removed.")
        else:
            print(f"No item found with SKU '{sku}'.")
        conn.close()

    def search_item(self, sku):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT sku, name, quantity, price FROM stock WHERE sku = ?", (sku,))
        row = cursor.fetchone()
        conn.close()

        if row:
            item = StockItem(row[1], row[0], row[2], row[3])
            print(item)
        else:
            print(f"No item found with SKU '{sku}'.")

    def search_value(self, sku):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity, price FROM stock WHERE sku = ?", (sku,))
        row = cursor.fetchone()
        conn.close()

        if row:
            name, quantity, price = row
            total_value = quantity * price
            print(f"The total value of '{name}' (SKU: {sku}) is ${total_value:.2f}")
        else:
            print(f"No item found with SKU '{sku}'.")

    def run(self):
        while True:
            try:
                userinput = int(input(
                    "Hello User, What would you like to do?\n"
                    "1. View stock\n"
                    "2. Add stock\n"
                    "3. Remove Stock\n"
                    "4. Search Stock\n"
                    "5. Search value\n"
                    "6. Exit\n"
                ))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if userinput == 1:
                self.view_stock()
            elif userinput == 2:
                name = input("Enter item name: ")
                sku = input("Insert SKU please, e.g. SKU001: ")
                try:
                    quantity = int(input("Enter quantity: "))
                    price = float(input("Enter price: "))
                except ValueError:
                    print("Invalid quantity or price input. Please enter valid numbers.")
                    continue
                self.add_item(name, sku, quantity, price)
            elif userinput == 3:
                sku = input("Enter SKU to remove, e.g. SKU001: ")
                self.remove_item(sku)
            elif userinput == 4:
                sku = input("Enter SKU to search, e.g. SKU001: ")
                self.search_item(sku)
            elif userinput == 5:
                sku = input("Enter SKU to find total value, e.g. SKU001: ")
                self.search_value(sku)
            elif userinput == 6:
                confirm = input("Are you sure you want to exit? (y/n): ").lower()
                if confirm == 'y':
                    print("Exiting...")
                    break
            else:
                print("Sorry, no valid option.")

if __name__ == "__main__":
    inventory = InventoryManagement()
    inventory.run()
