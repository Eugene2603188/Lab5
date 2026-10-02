import json

fail = 0
quit = 0
file_name = "Week 5/inventory.json"
history = []

def get_valid_input(quantity):
    global fail
    global quit

    while True:
        if quantity.lower() == "quit":
            quit = 1
            return "quit"
        elif quantity.isdigit():
            return int(quantity)
        else:
            print("Invalid input. Please enter a positive number or 'quit' to exit.")
            fail += 1
            quantity = input("Enter Quantity: ").strip()
    
def check_quantity_max(history_list, new_quantity):
    global fail

    current_total = sum(item["quantity"] for item in history_list)
    if current_total + new_quantity <= 500:
        return True
    else:
        print("Inventory limit exceeded. Cannot add more stock.")
        fail += 1
        return False

'''def calculate_tax(amount):
    tax_rate = 0.10
    tax_amount = amount * tax_rate
    return tax_amount
    
def generate_report(inventory, fail):
    print("Total Unit Processed:", inventory)
    print("Number of Failed/Rejected Entries:", fail)'''

def get_next_id(history_list):
    if len(history_list) > 0:
        return history_list[-1]["id"] + 1
    else:
        return 1001

#---- ALL DATA MANIPULATION FUNCTIONS -----
#Data Manipulation - Replaced previously print_current_orders()
def display_all(inventory):
    if not inventory:
        print("Inventory is currently empty.")
    else:
        print("-" * 40)
        print(f"{'ID':<10}{'Product Name':<20}{'Quantity':<10}")
        print("-" * 40)
        for item in inventory:
            print(f"{item['id']:<10}{item['name']:<20}{item['quantity']:<10}")
        print("-" * 40)

#Data Manipulation - Replaced previously add_order()
def add_product(inventory, product_name, quantity):
    next_id = get_next_id(inventory)
    new_product = {
        "id": next_id,
        "name": product_name,
        "quantity": quantity
    }
    inventory.append(new_product)
    print(f"Product '{product_name}' successfully added with ID {next_id}.")
    return new_product

#Data Manipulation - update_stock()
def update_stock(inventory, search_term, new_quantity):
    found = False
    for item in inventory:
        # Check if search_term matches the product name (case-insensitive) or product ID
        if str(item["id"]) == str(search_term) or item["name"].lower() == str(search_term).lower():
            item["quantity"] = new_quantity
            print(f"Stock updated! '{item['name']}' (ID: {item['id']}) new quantity is {item['quantity']}.")
            found = True
            break
            
    if not found:
        print(f"Product '{search_term}' not found in inventory.")

#Data Manipulation - search_product()
def search_product(inventory, search_term):
    found_items = []
    for item in inventory:
        if str(item["id"]) == str(search_term) or search_term.lower() in item["name"].lower():
            found_items.append(item)
            
    if found_items:
        print("\n--- Search Results ---")
        for item in found_items:
            print(f"ID: {item['id']} | Name: {item['name']} | Quantity: {item['quantity']}")
        print("----------------------\n")
    else:
        print(f"No products found matching '{search_term}'.\n")

#---- ALL DATA PERSISTENCE FUNCTIONS -----
#Data Persistence - Replaced previously persistence() + history_tracking() + load_inventory()
def load_inventory(file_name):
    try:
        with open(file_name, "r") as f:
            return json.load(f)  # Automatically parses JSON back into a list of dictionaries
    except FileNotFoundError:
        # Fallback default inventory if file doesn't exist
        return [
            {"id": 1001, "name": "Wireless Mouse", "quantity": 2},
            {"id": 1002, "name": "Keyboard", "quantity": 1},
            {"id": 1003, "name": "USB Cable", "quantity": 3}
        ]
    except json.JSONDecodeError:
        # Handles case if file exists but is empty/corrupted
        return []
    
#Data Persistence - Replaced previously save_inventory()
def save_inventory(file_name, history_list):
    try:
        with open(file_name, "w") as f:
            json.dump(history_list, f, indent=4)
        print(f"All orders successfully saved to {file_name}\n")
    except Exception as e:
        print(f"Error saving file: {e}\n")

print("Current Orders:\n")
history = load_inventory(file_name)
display_all(history)
print("\n")

while quit != 1:
    product_name = input("Enter Product Name: ").strip()

    if product_name.lower() == "quit":
        quit = 1
        break

    quantity = input("Enter Quantity: ").strip()
    valid_quantity = get_valid_input(quantity)

    if quit == 1 or valid_quantity == "quit":
        break

    if check_quantity_max(history, valid_quantity):
        new_item = add_product(history, product_name, valid_quantity)
        print(f"New Product Added:\n{new_item['id']}, {new_item['name']}, {new_item['quantity']}\n")

if len(history) > 0:
    save_inventory(file_name, history)
    print("All orders successfully saved to inventory.txt")

#Eugene Repo URL: https://github.com/Eugene2603188/Lab5

