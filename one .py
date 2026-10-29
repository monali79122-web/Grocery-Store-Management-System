import json
import os
from datetime import datetime

# File names used for saving data
INVENTORY_FILE = "inventory.json"   # stores current stock between runs
BILL_FILE = "bills.txt"             # every final bill is appended here

# Billing rules
DISCOUNT_LIMIT = 1000     # discount applies if subtotal >= Rs. 1000
DISCOUNT_PERCENT = 10     # discount percentage
GST_PERCENT = 5           # GST percentage on the discounted amount

# Starting inventory (used only when inventory.json does not exist yet)
DEFAULT_INVENTORY = {
    "Rice":  {"price": 50,  "stock": 100},   # per kg
    "Sugar": {"price": 45,  "stock": 50},    # per kg
    "Milk":  {"price": 30,  "stock": 40},    # per L
    "Oil":   {"price": 150, "stock": 20},    # per L
}


def load_inventory():
    """Load the saved stock from inventory.json if it exists,
    otherwise return a fresh copy of the default inventory."""
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r") as f:
            return json.load(f)
    return json.loads(json.dumps(DEFAULT_INVENTORY))  # a fresh copy


def save_inventory(inventory):
    """Write the current inventory (with updated stock) to inventory.json."""
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)


def find_item(inventory, name):
    """Case-insensitive search for an item.
    Returns the real item name (e.g. 'Rice') or None if not found."""
    for key in inventory:
        if key.lower() == name.strip().lower():
            return key
    return None


def view_stock(inventory):
    """Print every item with its remaining stock and price."""
    print("\n--- Current Stock ---")
    for name, info in inventory.items():
        print(f"{name}: {info['stock']}  (Price: Rs. {info['price']})")


def calculate_bill(cart, inventory):
    """Calculate the bill for the items in the cart.
    - subtotal: sum of price x quantity
    - discount: 10% of subtotal if subtotal >= 1000, else 0
    - gst: 5% of the amount after discount
    - total: amount after discount + gst
    Returns (subtotal, discount, gst, total)."""
    subtotal = sum(inventory[item]["price"] * qty for item, qty in cart)
    discount = subtotal * DISCOUNT_PERCENT / 100 if subtotal >= DISCOUNT_LIMIT else 0.0
    after_discount = subtotal - discount
    gst = after_discount * GST_PERCENT / 100
    total = after_discount + gst
    return subtotal, discount, gst, total


def discount_label(discount):
    """Return the label for the discount line.
    Shows the percentage only when a discount was actually given,
    e.g. 'Discount (10%)', otherwise just 'Discount'."""
    if discount > 0:
        return f"Discount ({DISCOUNT_PERCENT}%)"
    return "Discount"


def save_bill(cart, subtotal, discount, gst, total):
    """Append the final bill (date, items, subtotal, discount, GST, total)
    to bills.txt. Old bills are kept because the file is opened in append mode."""
    with open(BILL_FILE, "a") as f:
        f.write("=" * 35 + "\n")
        f.write(f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
        for item, qty in cart:
            f.write(f"{item} x {qty}\n")
        f.write(f"Subtotal: {subtotal:.2f}\n")
        f.write(f"{discount_label(discount)}: {discount:.2f}\n")
        f.write(f"GST ({GST_PERCENT}%): {gst:.2f}\n")
        f.write(f"Total: Rs. {total:.2f}\n")


def new_bill(inventory):
    """Create a new bill:
    1. Keep asking for item + quantity until the cashier types 'done'.
    2. Validate the item name, the quantity and the available stock.
    3. Calculate and print the bill.
    4. Reduce the stock, then save the inventory and the bill to files."""
    cart = []  # list of (item_name, quantity)
    print("\n--- New Bill --- (type 'done' as the item name to finish)")

    while True:
        name = input("Item: ").strip()
        if name.lower() == "done":
            break

        # Check that the item exists in the inventory
        item = find_item(inventory, name)
        if item is None:
            print(f"Item '{name}' not found in inventory.")
            continue

        # Check that the quantity is a positive whole number
        try:
            qty = int(input("Quantity: "))
        except ValueError:
            print("Invalid quantity. Enter a whole number.")
            continue
        if qty <= 0:
            print("Quantity must be greater than 0.")
            continue

        # Check stock, counting what is already in the cart for this item
        already_in_cart = sum(q for i, q in cart if i == item)
        available = inventory[item]["stock"] - already_in_cart
        if qty > available:
            print(f"Insufficient stock for {item}. Available: {available}")
            continue

        cart.append((item, qty))
        print(f"Added {qty} x {item}")

    if not cart:
        print("No items in cart. Bill cancelled.")
        return

    subtotal, discount, gst, total = calculate_bill(cart, inventory)

    # Print the bill on screen
    print("\n------ BILL ------")
    for item, qty in cart:
        print(f"{item} x {qty} = {inventory[item]['price'] * qty:.2f}")
    print(f"Subtotal: {subtotal:.2f}")
    print(f"{discount_label(discount)}: {discount:.2f}")
    print(f"GST ({GST_PERCENT}%): {gst:.2f}")
    print(f"Total: Rs. {total:.2f}")

    # Reduce stock, then save everything
    for item, qty in cart:
        inventory[item]["stock"] -= qty
    save_inventory(inventory)
    save_bill(cart, subtotal, discount, gst, total)
    print("Bill saved to bills.txt")


def main():
    """Show the main menu in a loop until the user chooses Exit."""
    inventory = load_inventory()
    while True:
        print("\n===== GROCERY STORE =====")
        print("1. New bill")
        print("2. View stock")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            new_bill(inventory)
        elif choice == "2":
            view_stock(inventory)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


main()