"""
generate_data.py
Generates realistic, internally-consistent sample data for Fulfillment Hub.
Run this once with: python generate_data.py
It creates 4 CSV files inside the data/ folder.
"""

import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)  # keeps the data the same every time we run this

# -----------------------------
# 1. PRODUCTS
# -----------------------------
products = [
    ("P101", "Wireless Mouse", "Black"),
    ("P101B", "Wireless Mouse", "White"),
    ("P102", "Mechanical Keyboard", "Standard"),
    ("P103", "USB-C Hub", "Silver"),
    ("P104", "Laptop Stand", "Grey"),
    ("P105", "Webcam HD", "Black"),
    ("P106", "Desk Lamp", "White"),
    ("P107", "Phone Charger 20W", "Black"),
    ("P108", "Bluetooth Speaker", "Blue"),
    ("P109", "Noise Cancelling Headphones", "Black"),
    ("P110", "Monitor Arm", "Silver"),
]

products_df = pd.DataFrame(products, columns=["sku", "product_name", "variant"])
products_df.to_csv("data/products.csv", index=False)

# -----------------------------
# 2. INVENTORY (per SKU, per warehouse)
# -----------------------------
inventory_rows = []
low_stock_skus = ["P103", "P108"]
out_of_stock_main_skus = ["P105"]
out_of_stock_everywhere_skus = ["P110"]

for sku, _, _ in products:
    if sku in out_of_stock_main_skus or sku in out_of_stock_everywhere_skus:
        main_stock = 0
    elif sku in low_stock_skus:
        main_stock = random.randint(1, 4)
    else:
        main_stock = random.randint(20, 120)

    reserved = random.randint(0, min(5, main_stock)) if main_stock > 0 else 0

    inventory_rows.append({
        "sku": sku,
        "warehouse": "main",
        "stock": main_stock,
        "reserved_stock": reserved,
    })

    if sku in out_of_stock_everywhere_skus:
        overflow_stock = 0
    elif sku in out_of_stock_main_skus:
        overflow_stock = random.randint(10, 30)
    else:
        overflow_stock = random.randint(0, 20)

    inventory_rows.append({
        "sku": sku,
        "warehouse": "overflow",
        "stock": overflow_stock,
        "reserved_stock": 0,
    })

inventory_df = pd.DataFrame(inventory_rows)
inventory_df["available_stock"] = inventory_df["stock"] - inventory_df["reserved_stock"]
inventory_df.to_csv("data/inventory.csv", index=False)

# -----------------------------
# 3. ORDERS
# -----------------------------
statuses_in_order = ["Order Received", "Processing", "Picking", "Packing", "Staging", "Shipped"]
couriers = ["SpeedEx", "QuickShip", "ParcelGo"]
customers = [f"Customer {i}" for i in range(1, 60)]

NUM_ORDERS = 100
today = datetime.now()

orders = []
for i in range(1, NUM_ORDERS + 1):
    order_id = f"ORD{1000 + i}"
    sku, product_name, variant = random.choice(products)
    qty = random.randint(1, 3)
    priority = random.random() < 0.2
    order_date = today - timedelta(days=random.randint(0, 3), hours=random.randint(0, 23))
    deadline = order_date + timedelta(hours=24 if priority else random.randint(48, 96))

    status = random.choices(
        statuses_in_order,
        weights=[10, 15, 25, 20, 15, 15],
        k=1
    )[0]

    main_row = inventory_df[(inventory_df.sku == sku) & (inventory_df.warehouse == "main")].iloc[0]
    is_blocked = (main_row["available_stock"] <= 0) and (statuses_in_order.index(status) < statuses_in_order.index("Picking"))
    if is_blocked:
        status = "Processing"

    is_delayed = (today > deadline) and (status != "Shipped")

    courier = random.choice(couriers)

    orders.append({
        "order_id": order_id,
        "customer": random.choice(customers),
        "order_date": order_date.strftime("%Y-%m-%d %H:%M"),
        "priority": priority,
        "deadline": deadline.strftime("%Y-%m-%d %H:%M"),
        "status": status,
        "sku": sku,
        "product_name": product_name,
        "variant": variant,
        "quantity": qty,
        "warehouse_location": "main",
        "courier": courier,
        "is_blocked_by_inventory": is_blocked,
        "is_delayed": is_delayed,
    })

orders_df = pd.DataFrame(orders)
orders_df.to_csv("data/orders.csv", index=False)

# -----------------------------
# 4. SHIPPING / STAGING
# -----------------------------
staging_locations = ["Staging A1", "Staging A2", "Staging B1"]
shipping_rows = []

for _, order in orders_df.iterrows():
    if order["status"] in ["Staging", "Shipped"]:
        pickup_time = pd.to_datetime(order["order_date"]) + timedelta(hours=random.randint(20, 90))
        if order["status"] == "Shipped":
            pickup_status = "Picked Up"
        else:
            roll = random.random()
            if roll < 0.1:
                pickup_status = "Missed"
            elif roll < 0.25:
                pickup_status = "At Risk"
            else:
                pickup_status = "Waiting"

        shipping_rows.append({
            "order_id": order["order_id"],
            "courier": order["courier"],
            "staging_location": random.choice(staging_locations),
            "pickup_time": pickup_time.strftime("%Y-%m-%d %H:%M"),
            "pickup_status": pickup_status,
        })

shipping_df = pd.DataFrame(shipping_rows)
shipping_df.to_csv("data/shipping.csv", index=False)

print("Done! Created 4 files inside data/:")
print("- products.csv:", len(products_df), "rows")
print("- inventory.csv:", len(inventory_df), "rows")
print("- orders.csv:", len(orders_df), "rows")
print("- shipping.csv:", len(shipping_df), "rows")