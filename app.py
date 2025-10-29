import streamlit as st
from pathlib import Path
from PIL import Image

# ---------------------------
# Homely Harvest - Streamlit App
# Single-file Streamlit app. Save as `app.py` and run:
#    pip install streamlit pillow
#    streamlit run app.py
# Replace images/ placeholders with your own images (see instructions below).
# ---------------------------

st.set_page_config(page_title="Homely Harvest", layout="wide", page_icon="🏡")

# --- Menu definition (edit prices, names, images here) ---
BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

MENU = {
    "Dry Coconut (Sukha Khobra)": {"price": 80, "image": IMAGES_DIR / "dry_coconut.jpg"},
    "Grated Coconut": {"price": 60, "image": IMAGES_DIR / "grated_coconut.jpg"},
    "Poha (Beaten Rice)": {"price": 50, "image": IMAGES_DIR / "poha.jpg"},
    "Roasted Peanuts": {"price": 70, "image": IMAGES_DIR / "peanuts.jpg"},
    "Groundnut Chikki": {"price": 40, "image": IMAGES_DIR / "chikki.jpg"},
    "Coconut Oil (Homemade)": {"price": 120, "image": IMAGES_DIR / "coconut_oil.jpg"},
    "Besan Ladoo": {"price": 90, "image": IMAGES_DIR / "besan_ladoo.jpg"},
}

# --- Helpers for session state cart ---
if "cart" not in st.session_state:
    st.session_state.cart = {}


def add_to_cart(item_name, qty=1):
    cart = st.session_state.cart
    if item_name in cart:
        cart[item_name] += qty
    else:
        cart[item_name] = qty
    st.session_state.cart = cart


def set_qty(item_name, qty):
    qty = int(qty)
    if qty <= 0:
        st.session_state.cart.pop(item_name, None)
    else:
        st.session_state.cart[item_name] = qty


def clear_cart():
    st.session_state.cart = {}


def cart_total():
    total = 0
    for item, qty in st.session_state.cart.items():
        price = MENU[item]["price"]
        total += price * qty
    return total

# --- Layout: Header ---
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://via.placeholder.com/100x100.png?text=HH", width=100)
with col2:
    st.markdown("# Homely Harvest")
    st.markdown("*Warm, homemade snacks & essentials — small-batch, made with love.*")

st.markdown("---")

# --- Main content: Menu items on left, Cart on right ---
menu_col, cart_col = st.columns([3, 1])

with menu_col:
    st.header("Menu")
    # show items in a grid
    items = list(MENU.items())
    cols_per_row = 2
    for i in range(0, len(items), cols_per_row):
        row = items[i : i + cols_per_row]
        cols = st.columns(len(row))
        for c, (name, meta) in zip(cols, row):
            with c:
                # show image if exists, else placeholder
                img_path = meta["image"]
                try:
                    if img_path.exists():
                        img = Image.open(img_path)
                        st.image(img, use_column_width=True, caption=name)
                    else:
                        # placeholder image
                        st.image("https://via.placeholder.com/300x180.png?text=" + name.replace(' ', '+'), use_column_width=True)
                except Exception:
                    st.image("https://via.placeholder.com/300x180.png?text=Image+Error", use_column_width=True)

                st.subheader(name)
                st.write(f"Price: ₹{meta['price']}")

                qty = st.number_input(f"Qty - {name}", min_value=0, step=1, key=f"qty_{name}")
                if st.button("Add to cart", key=f"add_{name}"):
                    if qty <= 0:
                        add_to_cart(name, 1)
                    else:
                        add_to_cart(name, qty)
                    st.success(f"Added {qty if qty>0 else 1} x {name} to cart")

with cart_col:
    st.header("Your Cart")
    if not st.session_state.cart:
        st.info("Cart is empty — add items from the menu.")
    else:
        for item, qty in list(st.session_state.cart.items()):
            price = MENU[item]["price"]
            col_a, col_b, col_c = st.columns([3, 1, 1])
            with col_a:
                st.write(item)
            with col_b:
                new_qty = st.number_input(f"qty_cart_{item}", min_value=0, value=int(qty), key=f"cart_{item}")
                if new_qty != qty:
                    set_qty(item, new_qty)
                    st.experimental_rerun()
            with col_c:
                st.write(f"₹{price * qty}")

        st.markdown("---")
        st.subheader(f"Total: ₹{cart_total()}")

        if st.button("Place Order"):
            # Simple order placement flow — in a real app you'd save to DB or send an email
            order_summary = "\n".join([f"{item} x{qty} = ₹{MENU[item]['price']*qty}" for item, qty in st.session_state.cart.items()])
            st.success("Thank you! Your order has been placed.")
            st.write("**Order summary:**")
            st.text(order_summary)
            st.balloons()
            clear_cart()

        if st.button("Clear Cart"):
            clear_cart()
            st.experimental_rerun()

# --- Footer: small note and instructions ---
st.markdown("---")
st.markdown("**Notes & customisation**:\n\n"
            "1. To change names/prices/images, edit the `MENU` dictionary at the top of this file.\n"
            "2. Put product images in a local `images/` folder next to this file and name them as referenced (e.g. `dry_coconut.jpg`).\n"
            "3. This example uses a very simple in-memory cart (Streamlit session state). For production, connect to a database or payment gateway.")

st.caption("Built with ❤️ for small home businesses — Homely Harvest")
