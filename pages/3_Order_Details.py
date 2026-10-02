import streamlit as st
import pandas as pd

st.set_page_config(page_title="Order Details - Fulfillment Hub", layout="wide")

# ---------- Style ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    div[data-testid="stSidebarNav"] { display: none; }
    section[data-testid="stSidebar"] {
        background-color: #10141c;
        border-right: 1px solid #2a2f3a;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Custom sidebar ----------
with st.sidebar:
    st.markdown("### 📦 Fulfillment Hub")
    st.page_link("Home.py", label="Home", icon="🏠")
    st.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
    st.page_link("pages/2_Orders.py", label="Orders", icon="📋")
    st.page_link("pages/3_Order_Details.py", label="Order Details", icon="🔎")
    st.page_link("pages/4_Inventory.py", label="Inventory", icon="📦")

# ---------- Load data ----------
orders = pd.read_csv("data/orders.csv")
shipping = pd.read_csv("data/shipping.csv")

st.title("🔎 Order Details")
st.caption("Select an order to see its full journey and update its status.")

st.write("")

# ---------- Order selector ----------
order_id = st.selectbox("Choose an Order ID", orders["order_id"].tolist())
order = orders[orders["order_id"] == order_id].iloc[0]

st.divider()

# ---------- Order summary ----------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**Order ID:** {order['order_id']}")
    st.markdown(f"**Customer:** {order['customer']}")
    st.markdown(f"**Order Date:** {order['order_date']}")
with col2:
    st.markdown(f"**Product:** {order['product_name']} ({order['variant']})")
    st.markdown(f"**Quantity:** {order['quantity']}")
    st.markdown(f"**Courier:** {order['courier']}")
with col3:
    priority_label = "⭐ Priority" if order["priority"] else "Regular"
    st.markdown(f"**Priority:** {priority_label}")
    st.markdown(f"**Deadline:** {order['deadline']}")
    if order["is_delayed"]:
        st.markdown("**Status flag:** 🔴 Delayed")
    elif order["is_blocked_by_inventory"]:
        st.markdown("**Status flag:** 🟠 Blocked by inventory")
    else:
        st.markdown("**Status flag:** ✅ On track")

st.divider()

# ---------- Fulfillment journey ----------
st.subheader("Fulfillment Journey")

stages = ["Order Received", "Processing", "Picking", "Packing", "Staging", "Shipped"]
current_index = stages.index(order["status"])

journey_html = "<div style='display:flex; gap:10px;'>"
for i, stage in enumerate(stages):
    if i < current_index:
        color, mark = "#4ade80", "✓"
    elif i == current_index:
        color, mark = "#60a5fa", "●"
    else:
        color, mark = "#4b5563", "○"
    journey_html += (
        "<div style='flex:1; text-align:center; padding:12px; background-color:#161b22; "
        "border-radius:10px; border:1px solid " + color + ";'>"
        "<div style='font-size:20px; color:" + color + ";'>" + mark + "</div>"
        "<div style='font-size:13px; color:" + color + "; margin-top:4px;'>" + stage + "</div>"
        "</div>"
    )
journey_html += "</div>"

st.markdown(journey_html, unsafe_allow_html=True)

if order["is_blocked_by_inventory"]:
    st.error(f"🚫 This order cannot move forward — SKU {order['sku']} is out of stock in the main warehouse.")

if order["status"] == "Picking":
    st.info(f"🔍 Before marking as Packed, double-check the picked item matches: **{order['product_name']} ({order['variant']})**, SKU **{order['sku']}**.")

# ---------- Shipping / staging info ----------
ship_row = shipping[shipping["order_id"] == order_id]
if len(ship_row) > 0:
    ship = ship_row.iloc[0]
    st.write("")
    st.subheader("🚚 Shipping & Staging")
    sc1, sc2, sc3 = st.columns(3)
    sc1.markdown(f"**Staging Location:** {ship['staging_location']}")
    sc2.markdown(f"**Pickup Time:** {ship['pickup_time']}")
    pickup_status = ship["pickup_status"]
    if pickup_status == "Missed":
        sc3.markdown("**Pickup Status:** 🔴 Missed")
        st.error("🚨 Courier pickup was missed for this order — needs immediate follow-up.")
    elif pickup_status == "At Risk":
        sc3.markdown("**Pickup Status:** 🟠 At Risk")
        st.warning("⏰ This pickup is at risk of being missed — check with the courier.")
    elif pickup_status == "Picked Up":
        sc3.markdown("**Pickup Status:** ✅ Picked Up")
    else:
        sc3.markdown("**Pickup Status:** 🔵 Waiting")

st.write("")

# ---------- Status update buttons ----------
st.subheader("Update Status")

if order["is_blocked_by_inventory"]:
    st.info("This order is blocked. Resolve the inventory issue before updating its status.")
else:
    next_index = current_index + 1
    if next_index < len(stages):
        next_stage = stages[next_index]
        if st.button(f"Mark as '{next_stage}'"):
            orders.loc[orders["order_id"] == order_id, "status"] = next_stage
            orders.to_csv("data/orders.csv", index=False)
            st.success(f"Order {order_id} moved to '{next_stage}'.")
            st.rerun()
    else:
        st.success("✅ This order has already been shipped.")