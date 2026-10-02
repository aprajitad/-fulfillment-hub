import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fulfillment Hub", page_icon="📦", layout="wide")

# ---------- Style ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2.5rem; }
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
total_orders = len(orders)
delayed_orders = len(orders[orders["is_delayed"] == True])
priority_orders = len(orders[orders["priority"] == True])

# ---------- Hero ----------
st.markdown("""
    <div style="padding-bottom: 6px;">
        <div style="font-size:44px; font-weight:800;">📦 Fulfillment Hub</div>
        <p style="font-size:17px; color:#9ca3af; margin-top:8px; max-width:650px;">
            A simple, operational tool for XYZ's warehouse and office team — see what's
            happening with every order, today, in one place.
        </p>
    </div>
""", unsafe_allow_html=True)

st.write("")

# ---------- Summary strip ----------
card_style = """
<div style="
    background-color:#161b22;
    padding:20px;
    border-radius:14px;
    text-align:center;
    border:1px solid #2a2f3a;
">
    <div style="font-size:30px; font-weight:800; color:{color};">{value}</div>
    <div style="font-size:14px; color:#9ca3af; margin-top:6px;">{label}</div>
</div>
"""

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(card_style.format(color="#ffffff", value=total_orders, label="📦 Orders Today"), unsafe_allow_html=True)
with col2:
    st.markdown(card_style.format(color="#facc15", value=priority_orders, label="⭐ Priority Orders"), unsafe_allow_html=True)
with col3:
    color = "#f87171" if delayed_orders > 0 else "#4ade80"
    st.markdown(card_style.format(color=color, value=delayed_orders, label="⚠️ Delayed Orders"), unsafe_allow_html=True)

st.write("")
st.write("")

# ---------- Clickable feature cards ----------
st.markdown("<div style='font-size:22px; font-weight:700; margin-bottom:10px;'>What you can do here</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    with st.container(border=True):
        st.page_link("pages/1_Dashboard.py", label="🏠 Dashboard", icon=None)
        st.caption("See today's fulfillment health at a glance, and what needs attention first.")
    with st.container(border=True):
        st.page_link("pages/2_Orders.py", label="📋 Orders", icon=None)
        st.caption("Search, filter, and open any order to see its full details.")

with c2:
    with st.container(border=True):
        st.page_link("pages/3_Order_Details.py", label="🔎 Order Details", icon=None)
        st.caption("Open a specific order to see its journey and update its status.")
    with st.container(border=True):
        st.page_link("pages/4_Inventory.py", label="📦 Inventory", icon=None)
        st.caption("Spot low-stock and out-of-stock items before they block an order.")

st.write("")
st.caption("👈 Use the sidebar to navigate between pages.")