# Grocery Store Management System

**Problem Statement No:** 72
**University:** Rungta International Skills University, School of Information Technology (BCA)
**Language:** Python 3
**Concepts used:** Lists, Dictionaries, Functions, Billing, File Handling

## About the Project

A console-based billing application for a grocery store. The cashier selects items and quantities from the inventory. The program calculates the subtotal, discount, GST and final bill, reduces the stock, and saves every bill in a file.

## Features

- Menu-driven console application (New bill, View stock, Exit)
- Inventory stored as a dictionary; the current cart is stored as a list
- Case-insensitive item search (`rice`, `RICE` and `Rice` all work)
- Validation for unknown items, invalid quantities and insufficient stock
- Stock is reduced after every bill and saved in `inventory.json`
- Every bill is appended to `bills.txt` with date and time

## Billing Rules

| Rule | Value |
|------|-------|
| Discount | 10% if subtotal is Rs. 1000 or more, otherwise 0 |
| GST | 5% on the amount after discount |
| Total | (Subtotal - Discount) + GST |

## Default Inventory

| Item | Price | Stock |
|------|-------|-------|
| Rice | Rs. 50 per kg | 100 |
| Sugar | Rs. 45 per kg | 50 |
| Milk | Rs. 30 per L | 40 |
| Oil | Rs. 150 per L | 20 |

## How to Run

1. Install Python 3.
2. Download or clone this repository.
3. Open a terminal in the project folder and run:

```
python grocery_store.py
```

## Project Files

| File | Purpose |
|------|---------|
| `grocery_store.py` | Main program |
| `inventory.json` | Saved stock (created automatically on the first bill) |
| `bills.txt` | All saved bills (created automatically on the first bill) |

## Functions

| Function | Description |
|----------|-------------|
| `load_inventory()` | Loads saved stock, or the default inventory if no file exists |
| `save_inventory()` | Saves the updated stock to `inventory.json` |
| `find_item()` | Case-insensitive search for an item in the inventory |
| `view_stock()` | Prints the current stock and prices |
| `calculate_bill()` | Calculates subtotal, discount, GST and total |
| `discount_label()` | Returns `Discount (10%)` when a discount applies, otherwise `Discount` |
| `save_bill()` | Appends the final bill to `bills.txt` |
| `new_bill()` | Takes items, validates input, prints the bill and updates the stock |
| `main()` | Shows the main menu and runs the program loop |

## Test Cases

### Test Case 1: Normal Input
**Input:** Menu option 1 (New bill), Rice: 2, Milk: 3

**Output:**
```
Subtotal: 190.00
Discount: 0.00
GST (5%): 9.50
Total: Rs. 199.50
```

### Test Case 2: Boundary / Minimum Input
**Input:** Menu option 1 (New bill), Oil: 4, Rice: 8 (subtotal exactly 1000)

**Output:**
```
Subtotal: 1000.00
Discount (10%): 100.00
GST (5%): 45.00
Total: Rs. 945.00
```

### Test Case 3: Invalid Input
**Input:** Menu option 1 (New bill), Item: Butter, Quantity: 2, Item: Milk, Quantity: 50

**Output:**
```
Item 'Butter' not found in inventory.
Insufficient stock for Milk. Available: 40
```

### Test Case 4: Different Valid Scenario
**(a) Input:** Menu option 1 (New bill), Sugar: 10, Milk: 5

**Output:**
```
Subtotal: 600.00
Discount: 0.00
GST (5%): 30.00
Total: Rs. 630.00
```

**(b) Input:** Menu option 2 (View stock)

**Output:**
```
Rice: 100
Sugar: 40
Milk: 35
Oil: 20
```

> Note: The test cases assume a fresh inventory. Delete `inventory.json` before running each test case to reset the stock.

## Sample Bill in bills.txt

```
===================================
Date: 30-10-2026 01:10:00
Oil x 4
Rice x 8
Subtotal: 1000.00
Discount (10%): 100.00
GST (5%): 45.00
Total: Rs. 945.00
```

## Author

Name: Monali Kumari
Enrollment No: 00582
