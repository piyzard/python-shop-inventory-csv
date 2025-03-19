import csv
from tabulate import tabulate

class Shop:
    def __init__(self):
        self.inv = {}  
        self.inv_file = "inventory.csv" 
        self.sales_file = "sales.csv"  
        try:
            with open(self.inv_file, newline='') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row:
                        self.inv[row[0]] = [row[1], float(row[2]), int(row[3])]
        except FileNotFoundError:
            open(self.inv_file, 'w').close()


    def save(self):
        with open(self.inv_file, 'w', newline='') as f:
            csv.writer(f).writerows([[k, *v] for k, v in self.inv.items()])

    def menu(self):
        while (c := input("\n1. View Inventory\n2. Add Product\n3. Process Sale\n4. View Sales\n5. Exit\n\nChoice: ")) != "5":
            {"1": self.view, "2": self.add, "3": self.sale, "4": self.report}.get(c, lambda: print("Invalid"))()
    
    def view(self):
        print(tabulate([[k, *v] for k, v in self.inv.items()], headers=["ID", "Name", "Price", "Stock"], tablefmt="grid"))
    
    def add(self):
        self.inv[input("ID: ")] = [input("Name: "), float(input("Price: ")), int(input("Stock: "))]
        self.save()
    
    def sale(self):
        sid, items = input("Sale ID: "), []
        while True:
            pid = input("Product ID (or 'done'): ")
            if pid == "done":
                break 
            if pid in self.inv:
                try:
                    qty = int(input(f"Quantity for {self.inv[pid][0]}: "))
                    if qty <= self.inv[pid][2]:
                        self.inv[pid][2] -= qty
                        items.append([pid, self.inv[pid][0], qty, self.inv[pid][1]])
                    else:
                        print("Insufficient stock!")
                except ValueError:
                    print("Invalid quantity! Please enter a valid number.")
            else:
                print("Invalid product ID!")
        with open(self.sales_file, 'a', newline='') as f:
            csv.writer(f).writerows([[sid, *i, i[1] * i[2]] for i in items])
        self.save()

    
    def report(self):
        try:
            with open(self.sales_file, newline='') as f:
                print(tabulate([row for row in csv.reader(f)], headers=["Sale ID", "Product ID", "Name", "Quantity", "Total"], tablefmt="grid"))
        except FileNotFoundError:
            print("No sales recorded.")

if __name__ == "__main__":
    Shop().menu()
