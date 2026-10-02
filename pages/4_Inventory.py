import streamlit as st
import pandas as pd

st.set_page_config(page_title="Inventory - Fulfillment Hub", layout="wide")

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
inventory = pd.read_csv("data/inventory.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")

st.title("📦 Inventory")
st.caption("Stock levels across both warehouses, and which orders they're blocking.")

st.write("")

# ---------- Build a per-SKU summary (main + overflow combined) ----------
main_inv = inventory[inventory["warehouse"] == "main"].set_index("sku")
overflow_inv = inventory[inventory["warehouse"] == "overflow"].set_index("sku")

summary_rows = []
for _, prod in products.iterrows():
    sku = prod["sku"]
    main_available = main_inv.loc[sku, "available_stock"] if sku in main_inv.index else 0
    overflow_available = overflow_inv.loc[sku, "available_stock"] if sku in overflow_inv.index else 0

    if main_available <= 0 and overflow_available > 0:
        inv_status = "🟠 Out in main (stock in overflow)"
    elif main_available <= 0:
        inv_status = "🔴 Out of stock"
    elif main_available <= 5:
        inv_status = "🟡 Low stock"
    else:
        inv_status = "🟢 In stock"

    summary_rows.append({
        "SKU": sku,
        "Product": prod["product_name"],
        "Variant": prod["variant"],
        "Main Warehouse Stock": main_available,
        "Overflow Warehouse Stock": overflow_available,
        "Status": inv_status,
    })

summary_df = pd.DataFrame(summary_rows)

# ---------- KPI row ----------
out_of_stock_count = len(summary_df[summary_df["Status"] == "🔴 Out of stock"])
low_stock_count = len(summary_df[summary_df["Status"] == "🟡 Low stock"])
needs_transfer_count = len(summary_df[summary_df["Status"] == "🟠 Out in main (stock in overflow)"])

col1, col2, col3 = st.columns(3)
card_style = """
<div style="background-color:#161b22; padding:18px; border-radius:12px; text-align:center; border:1px solid #2a2f3a;">
    <div style="font-size:26px; font-weight:700; color:{color};">{value}</div>
    <div style="font-size:14px; color:#9ca3af; margin-top:4px;">{label}</div>
</div>
"""
with col1:
    st.markdown(card_style.format(color="#f87171" if out_of_stock_count else "#4ade80", value=out_of_stock_count, label="🔴 Out of Stock SKUs"), unsafe_allow_html=True)
with col2:
    st.markdown(card_style.format(color="#facc15" if low_stock_count else "#4ade80", value=low_stock_count, label="🟡 Low Stock SKUs"), unsafe_allow_html=True)
with col3:
    st.markdown(card_style.format(color="#fb923c" if needs_transfer_count else "#4ade80", value=needs_transfer_count, label="🟠 Needs Transfer from Overflow"), unsafe_allow_html=True)

st.write("")
st.caption("'Needs Transfer' means stock exists, but it's sitting in the overflow warehouse and hasn't been moved to the main warehouse yet — so it still can't be picked.")

st.divider()

# ---------- Inventory table ----------
st.subheader("Stock by product")
st.dataframe(summary_df, use_container_width=True, hide_index=True)

st.divider()

# ---------- Orders blocked by inventory ----------
# ---------- Orders blocked by inventory ----------
st.subheader("🚫 Orders Blocked by Inventory")
st.caption("These orders can't move forward until stock is restocked or transferred from the overflow warehouse.")

blocked = orders[orders["is_blocked_by_inventory"] == True]

if len(blocked) == 0:
    st.success("✅ No orders are currently blocked by inventory.")
else:
    for _, row in blocked.iterrows():
        st.error(
            f"Order **{row['order_id']}** ({row['customer']}) is blocked — "
            f"SKU **{row['sku']}** ({row['product_name']}, {row['variant']}) is out of stock in the main warehouse."
        )