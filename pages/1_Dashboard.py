import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard - Fulfillment Hub", layout="wide")

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
shipping = pd.read_csv("data/shipping.csv")

# ---------- Calculate KPIs ----------
total_orders = len(orders)
pending_orders = len(orders[orders["status"] != "Shipped"])
priority_orders = len(orders[orders["priority"] == True])
delayed_orders = len(orders[orders["is_delayed"] == True])
blocked_orders = len(orders[orders["is_blocked_by_inventory"] == True])
priority_at_risk = orders[(orders["priority"] == True) & (orders["is_delayed"] == True)]
pickup_issues = shipping[shipping["pickup_status"].isin(["Missed", "At Risk"])]

# ---------- Header ----------
st.title("🏠 Dashboard")
st.caption("A quick look at today's fulfillment situation — refreshed every time you open this page.")

st.write("")

# ---------- KPI Cards ----------
st.subheader("Today at a glance")

card_style = """
<div style="
    background-color:#161b22;
    padding:18px;
    border-radius:12px;
    text-align:center;
    border:1px solid #2a2f3a;
">
    <div style="font-size:26px; font-weight:700; color:{color};">{value}</div>
    <div style="font-size:14px; color:#9ca3af; margin-top:4px;">{label}</div>
</div>
"""

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(card_style.format(color="#ffffff", value=total_orders, label="📦 Total Orders"), unsafe_allow_html=True)
with col2:
    st.markdown(card_style.format(color="#ffffff", value=pending_orders, label="⏳ Pending Orders"), unsafe_allow_html=True)
with col3:
    st.markdown(card_style.format(color="#facc15", value=priority_orders, label="⭐ Priority Orders"), unsafe_allow_html=True)
with col4:
    color4 = "#f87171" if delayed_orders > 0 else "#4ade80"
    st.markdown(card_style.format(color=color4, value=delayed_orders, label="⚠️ Delayed Orders"), unsafe_allow_html=True)
with col5:
    color5 = "#f87171" if blocked_orders > 0 else "#4ade80"
    st.markdown(card_style.format(color=color5, value=blocked_orders, label="🚫 Blocked by Inventory"), unsafe_allow_html=True)

st.write("")
st.caption("These numbers are calculated live from the order data — nothing here is fixed or hardcoded.")

st.divider()

# ---------- Attention Required ----------
st.subheader("⚠️ Attention Required")
st.caption("The issues most likely to cause a late or wrong delivery today, so they don't get missed.")

alert_style = """
<div style="
    background-color:{bg};
    border-left:5px solid {border};
    padding:14px 18px;
    border-radius:8px;
    margin-bottom:10px;
    color:{text};
    font-size:15px;
">
    {message}
</div>
"""

if delayed_orders == 0 and blocked_orders == 0 and len(priority_at_risk) == 0 and len(pickup_issues) == 0:
    st.markdown(alert_style.format(bg="#14301f", border="#4ade80", text="#86efac", message="✅ No urgent issues right now — everything is on track."), unsafe_allow_html=True)
else:
    if len(priority_at_risk) > 0:
        st.markdown(alert_style.format(bg="#3b1414", border="#f87171", text="#fca5a5", message=f"🔴 {len(priority_at_risk)} PRIORITY order(s) have missed their deadline — handle these first."), unsafe_allow_html=True)
    if delayed_orders > 0:
        st.markdown(alert_style.format(bg="#3b2a14", border="#fb923c", text="#fdba74", message=f"🟠 {delayed_orders} order(s) overall are delayed past their deadline."), unsafe_allow_html=True)
    if blocked_orders > 0:
        st.markdown(alert_style.format(bg="#3b2a14", border="#fb923c", text="#fdba74", message=f"🟠 {blocked_orders} order(s) are blocked because required stock isn't available in the main warehouse."), unsafe_allow_html=True)
    if len(pickup_issues) > 0:
        st.markdown(alert_style.format(bg="#3b2a14", border="#fb923c", text="#fdba74", message=f"🟠 {len(pickup_issues)} courier pickup(s) are missed or at risk — check Shipping details on each order."), unsafe_allow_html=True)