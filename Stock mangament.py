import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Management System")

        # Connect to DB and create table if not exists
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                sku TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)
        self.conn.commit()

        # UI Setup
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Table
        self.tree = ttk.Treeview(self.root, columns=('SKU', 'Name', 'Quantity', 'Price'), show='headings')
        self.tree.heading('SKU', text='SKU')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Price', text='Price')
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Buttons
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Add Item", command=self.add_item_popup).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Delete by SKU", command=self.delete_item_popup).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Search SKU", command=self.search_item_popup).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Exit", command=self.root.destroy).pack(side=tk.LEFT, padx=5)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT sku, name, quantity, price FROM stock")
        for item in self.cursor.fetchall():
            self.tree.insert('', tk.END, values=item)

    def add_item_popup(self):
        def submit():
            sku = sku_entry.get()
            name = name_entry.get()
            try:
                quantity = int(quantity_entry.get())
                price = float(price_entry.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Quantity must be an integer and price a number.")
                return
            try:
                self.cursor.execute("INSERT INTO stock (sku, name, quantity, price) VALUES (?, ?, ?, ?)",
                                    (sku, name, quantity, price))
                self.conn.commit()
                self.load_data()
                top.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate SKU", "An item with this SKU already exists.")

        top = tk.Toplevel(self.root)
        top.title("Add New Item")

        tk.Label(top, text="SKU:").grid(row=0, column=0)
        sku_entry = tk.Entry(top)
        sku_entry.grid(row=0, column=1)

        tk.Label(top, text="Name:").grid(row=1, column=0)
        name_entry = tk.Entry(top)
        name_entry.grid(row=1, column=1)

        tk.Label(top, text="Quantity:").grid(row=2, column=0)
        quantity_entry = tk.Entry(top)
        quantity_entry.grid(row=2, column=1)

        tk.Label(top, text="Price:").grid(row=3, column=0)
        price_entry = tk.Entry(top)
        price_entry.grid(row=3, column=1)

        tk.Button(top, text="Submit", command=submit).grid(row=4, column=0, columnspan=2)

    def delete_item_popup(self):
        def submit():
            sku = sku_entry.get()
            self.cursor.execute("DELETE FROM stock WHERE sku = ?", (sku,))
            if self.cursor.rowcount == 0:
                messagebox.showinfo("Not found", "No item with that SKU.")
            else:
                self.conn.commit()
                self.load_data()
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Delete Item")

        tk.Label(top, text="Enter SKU to delete:").grid(row=0, column=0)
        sku_entry = tk.Entry(top)
        sku_entry.grid(row=0, column=1)
        tk.Button(top, text="Delete", command=submit).grid(row=1, column=0, columnspan=2)

    def search_item_popup(self):
        def submit():
            sku = sku_entry.get()
            self.cursor.execute("SELECT * FROM stock WHERE sku = ?", (sku,))
            item = self.cursor.fetchone()
            if item:
                total_value = item[2] * item[3]
                messagebox.showinfo("Item Found",
                                    f"Name: {item[1]}\nSKU: {item[0]}\nQuantity: {item[2]}\nPrice: {item[3]:.2f}\nTotal Value: ${total_value:.2f}")
            else:
                messagebox.showinfo("Not Found", "No item found with that SKU.")
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Search Item")

        tk.Label(top, text="Enter SKU:").grid(row=0, column=0)
        sku_entry = tk.Entry(top)
        sku_entry.grid(row=0, column=1)
        tk.Button(top, text="Search", command=submit).grid(row=1, column=0, columnspan=2)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
