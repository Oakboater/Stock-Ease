import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import csv

DB_PATH = os.path.join(os.path.dirname(__file__), 'inventory.db')

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Management System")
        self.root.geometry("800x600")  # Better default size

        # Connect to DB
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.setup_ui()
        self.load_data()
        
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                sku TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)
        self.conn.commit()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Table with scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=('SKU', 'Name', 'Quantity', 'Price'), show='headings')
        self.tree.heading('SKU', text='SKU')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Price', text='Price')
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure tags for low stock
        self.tree.tag_configure('lowstock', background='#ffcccc')

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Add Item", command=self.add_item_popup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Item", command=self.edit_item_popup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete by SKU", command=self.delete_item_popup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search SKU", command=self.search_item_popup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export CSV", command=self.export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)

    def load_data(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Fetch and display data
        self.cursor.execute("SELECT sku, name, quantity, price FROM stock")
        for item in self.cursor.fetchall():
            tags = 'lowstock' if item[2] < 5 else ''
            self.tree.insert('', tk.END, values=item, tags=tags)

    def add_item_popup(self):
        top = tk.Toplevel(self.root)
        top.title("Add New Item")
        top.grab_set()  # Make modal
        top.resizable(False, False)
        
        ttk.Label(top, text="SKU:").grid(row=0, column=0, padx=5, pady=5)
        sku_entry = ttk.Entry(top)
        sku_entry.grid(row=0, column=1, padx=5, pady=5)
        sku_entry.focus()

        ttk.Label(top, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(top)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(top, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
        quantity_entry = ttk.Entry(top)
        quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(top, text="Price:").grid(row=3, column=0, padx=5, pady=5)
        price_entry = ttk.Entry(top)
        price_entry.grid(row=3, column=1, padx=5, pady=5)

        def submit():
            sku = sku_entry.get()
            name = name_entry.get()
            try:
                quantity = int(quantity_entry.get())
                price = float(price_entry.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Quantity must be integer, price must be number")
                return
                
            try:
                self.cursor.execute(
                    "INSERT INTO stock (sku, name, quantity, price) VALUES (?, ?, ?, ?)",
                    (sku, name, quantity, price)
                )
                self.conn.commit()
                self.load_data()
                top.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate SKU", "SKU already exists!")

        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Submit", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=top.destroy).pack(side=tk.LEFT, padx=5)

    def edit_item_popup(self):
        selected = self.tree.selection()
        if not selected: 
            messagebox.showwarning("Warning", "Select an item first!")
            return
        
        item_data = self.tree.item(selected[0])['values']
        sku = item_data[0]
        
        top = tk.Toplevel(self.root)
        top.title("Edit Item")
        top.grab_set()
        top.resizable(False, False)
        
        ttk.Label(top, text="SKU:").grid(row=0, column=0, padx=5, pady=5)
        sku_label = ttk.Label(top, text=sku)
        sku_label.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(top)
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        name_entry.insert(0, item_data[1])

        ttk.Label(top, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
        quantity_entry = ttk.Entry(top)
        quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        quantity_entry.insert(0, item_data[2])

        ttk.Label(top, text="Price:").grid(row=3, column=0, padx=5, pady=5)
        price_entry = ttk.Entry(top)
        price_entry.grid(row=3, column=1, padx=5, pady=5)
        price_entry.insert(0, item_data[3])

        def submit():
            try:
                name = name_entry.get()
                quantity = int(quantity_entry.get())
                price = float(price_entry.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Check number formats")
                return
                
            self.cursor.execute(
                "UPDATE stock SET name=?, quantity=?, price=? WHERE sku=?",
                (name, quantity, price, sku)
            )
            self.conn.commit()
            self.load_data()
            top.destroy()

        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Update", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=top.destroy).pack(side=tk.LEFT, padx=5)

    def delete_item_popup(self):
        top = tk.Toplevel(self.root)
        top.title("Delete Item")
        top.grab_set()
        top.resizable(False, False)
        
        ttk.Label(top, text="Enter SKU to delete:").grid(row=0, column=0, padx=5, pady=5)
        sku_entry = ttk.Entry(top)
        sku_entry.grid(row=0, column=1, padx=5, pady=5)
        sku_entry.focus()

        def submit():
            sku = sku_entry.get()
            self.cursor.execute("DELETE FROM stock WHERE sku=?", (sku,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                self.load_data()
                messagebox.showinfo("Success", "Item deleted")
            else:
                messagebox.showinfo("Not found", "SKU does not exist")
            top.destroy()

        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Delete", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=top.destroy).pack(side=tk.LEFT, padx=5)

    def search_item_popup(self):
        top = tk.Toplevel(self.root)
        top.title("Search Item")
        top.grab_set()
        top.resizable(False, False)
        
        ttk.Label(top, text="Enter SKU:").grid(row=0, column=0, padx=5, pady=5)
        sku_entry = ttk.Entry(top)
        sku_entry.grid(row=0, column=1, padx=5, pady=5)
        sku_entry.focus()

        def submit():
            sku = sku_entry.get()
            self.cursor.execute("SELECT * FROM stock WHERE sku=?", (sku,))
            item = self.cursor.fetchone()
            
            if item:
                total_value = item[2] * item[3]
                messagebox.showinfo("Item Found",
                    f"SKU: {item[0]}\nName: {item[1]}\n"
                    f"Quantity: {item[2]}\nPrice: €{item[3]:.2f}\n"
                    f"Total Value: €{total_value:.2f}")
            else:
                messagebox.showinfo("Not Found", "No item with that SKU")
            top.destroy()

        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Search", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=top.destroy).pack(side=tk.LEFT, padx=5)

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['SKU', 'Name', 'Quantity', 'Price'])
                    self.cursor.execute("SELECT * FROM stock")
                    writer.writerows(self.cursor.fetchall())
                messagebox.showinfo("Success", f"Exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Failed", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
