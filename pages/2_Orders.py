import streamlit as st
import pandas as pd

st.set_page_config(page_title="Orders - Fulfillment Hub", layout="wide")

# ---------- Style: font + hide default nav ----------
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

# ---------- Custom sidebar (same on every page) ----------
with st.sidebar:
    st.markdown("### 📦 Fulfillment Hub")
    st.page_link("Home.py", label="Home", icon="🏠")
    st.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
    st.page_link("pages/2_Orders.py", label="Orders", icon="📋")
    st.page_link("pages/3_Order_Details.py", label="Order Details", icon="🔎")
    st.page_link("pages/4_Inventory.py", label="Inventory", icon="📦")

# ---------- Load data ----------
orders = pd.read_csv("data/orders.csv")

# ---------- Header ----------
st.title("📋 Orders")
st.caption("Search and filter every order, and see its status at a glance.")

st.write("")

# ---------- Filters ----------
st.subheader("Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    status_options = ["All"] + sorted(orders["status"].unique().tolist())
    status_filter = st.selectbox("Status", status_options)

with col2:
    priority_filter = st.selectbox("Priority", ["All", "Priority only", "Regular only"])

with col3:
    issue_filter = st.selectbox("Issue", ["All", "Delayed only", "Blocked by inventory only"])

with col4:
    search_id = st.text_input("Search Order ID or Customer")

# ---------- Apply filters ----------
filtered = orders.copy()

if status_filter != "All":
    filtered = filtered[filtered["status"] == status_filter]

if priority_filter == "Priority only":
    filtered = filtered[filtered["priority"] == True]
elif priority_filter == "Regular only":
    filtered = filtered[filtered["priority"] == False]

if issue_filter == "Delayed only":
    filtered = filtered[filtered["is_delayed"] == True]
elif issue_filter == "Blocked by inventory only":
    filtered = filtered[filtered["is_blocked_by_inventory"] == True]

if search_id:
    filtered = filtered[
        filtered["order_id"].str.contains(search_id, case=False, na=False) |
        filtered["customer"].str.contains(search_id, case=False, na=False)
    ]

# Sort so priority + delayed/blocked orders surface at the top by default
filtered = filtered.sort_values(
    by=["is_delayed", "priority", "is_blocked_by_inventory"],
    ascending=[False, False, False]
)

st.write("")
st.caption(f"Showing {len(filtered)} of {len(orders)} orders — delayed and priority orders are shown first.")

# ---------- Display table with friendly labels ----------
display_df = filtered.copy()
display_df["Priority"] = display_df["priority"].apply(lambda x: "⭐ Priority" if x else "Regular")
display_df["Issue"] = display_df.apply(
    lambda r: "🔴 Delayed" if r["is_delayed"] else ("🟠 Blocked" if r["is_blocked_by_inventory"] else "—"),
    axis=1
)

st.dataframe(
    display_df[[
        "order_id", "customer", "order_date", "Priority", "status",
        "product_name", "variant", "quantity", "deadline", "courier", "Issue"
    ]].rename(columns={
        "order_id": "Order ID",
        "customer": "Customer",
        "order_date": "Order Date",
        "status": "Status",
        "product_name": "Product",
        "variant": "Variant",
        "quantity": "Qty",
        "deadline": "Deadline",
        "courier": "Courier",
    }),
    use_container_width=True,
    hide_index=True,
    height=450,
)