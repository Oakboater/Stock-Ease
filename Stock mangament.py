class StockItem:
    def __init__(self, name, sku, quantity, price):
        self.name = name
        self.sku = sku
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"Name: {self.name}, SKU: {self.sku}, Quantity: {self.quantity}, Price: ${self.price:.2f}"



class InventoryManagement:
    def __init__(self):
        self.stock_items = [
            StockItem("EGG", "SKU001", 12, 6),
            StockItem("Banana", "SKU002", 24, 0.5),
            StockItem("Meat", "SKU003", 20, 6),
        ]

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
                if userinput not in range(1, 7):
                    print("Sorry, no valid Option")
                elif userinput == 1:
                    for item in self.stock_items:
                        print(item)
    
    
    
    
                elif userinput == 2:
                    name = input("Enter item name: ")
                    sku = input("Insert SKU please, E.g SKU001: ")
                    quantity = int(input("Enter quantity: "))
                    price = float(input("Enter price: "))
                    self.stock_items.append(StockItem(name, sku, quantity, price))
                    print("Item added successfully.")
    
    
    
                elif userinput == 3:
                    removesku = input("Enter SKU e.g SKU001: ")
                    removed = False
                    for item in self.stock_items:
                        if item.sku == removesku:
                            self.stock_items.remove(item)
                            print(f"Item with SKU {removesku} removed.")
                            removed = True
                            break
                    if not removed:
                        print(f"No item found with SKU {removesku}.")
    
    
    
                elif userinput == 4:
                    searchsku = input("Enter SKU for item search: ")
                    found = False
                    for item in self.stock_items:
                        if item.sku.lower() == searchsku.lower():
                            print(item)
                            found = True
                            break
                    if not found:
                        print(f"Couldn't find item with SKU {searchsku}")

                elif userinput == 5:
                    searchsku = input("Enter SKU for value search:")
                    for item in self.stock_items:
                        if item.sku.lower() == searchsku.lower():
                            print(f"The value for the product {item} is {item.price * item.quantity}")
                        
                    
    
    
    
    
    
                elif userinput == 6:
                    ays = input("Are you sure? y/n?").lower()
                    if ays == "y":
                        print("Exiting...")
                        return
                else: 
                    print("Welcome back!")


inventory = InventoryManagement()
inventory.run()
