import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import base64

st.set_page_config(layout="wide")
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #f4f1ea;
    }
    [data-testid=stSidebar] {
        background-color: #2c3e50;
        color: white;
    }
    [data-testid="stSidebar"] h1 {
        color: white;
    }
    [data-testid="stSidebar"] h3 {
        color: white;
    }
    [data-testid="stSidebar"] button {
        background-color: #2c3e50;
        border-color: #f4f1ea;
    }
    .cart-item {
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
    }
    .custom-container {
        background-color: #2c3e50;
        color: white;
        padding: 20px;
        margin-top: 20px;
        height: 55vh;
        border-radius: 10px;
        text-align: center;
    }
    .custom-container h4 {
        margin-left: 23px; 
        color: white;
        
    }
    .custom-container h5{
        color: white;
        
    }
    .remove-button {
        color: red;
        font-size: 20px;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Define a list of clothing items, their prices, and images
clothing_items = [
    # T-Shirts
    {"name": "Black Bunny Print T-Shirt", "price": 500, "rating": 4, "image": "images/Tshirt/t1.png"},
    {"name": "Pink Cat Paw T-Shirt", "price": 550, "rating": 3, "image": "images/Tshirt/t2.png"},
    {"name": "Queen Lettering Pink T-Shirt", "price": 600, "rating": 4, "image": "images/Tshirt/t3.png"},
    {"name": "White Girl Graphic T-Shirt", "price": 650, "rating": 5, "image": "images/Tshirt/t4.png"},
    # {"name": "Maroon Heart Patch T-Shirt", "price": 700, "rating": 4, "image": "images/Tshirt/t5.png"},
    
    # Jeans
    {"name": "Light Blue Wide-Leg Jeans", "price": 1200, "rating": 3, "image": "images/Jeans/j1.png"},
    {"name": "Black Flared Jeans", "price": 1250, "rating": 4, "image": "images/Jeans/j2.png"},
    {"name": "Dark Blue High-Waisted Jeans", "price": 1300, "rating": 5, "image": "images/Jeans/j3.png"},
    # {"name": "Light Blue Skinny Jeans", "price": 1350, "rating": 5, "image": "images/Jeans/j4.png"},
    # {"name": "Grey Straight-Leg Jeans", "price": 1400, "rating": 3, "image": "images/Jeans/j5.png"},
    
    # Shoes
    {"name": "Chunky White Sneakers", "price": 3000, "rating": 5, "image": "images/Shoes/s1.png"},
    {"name": "Black and Neon Green Sport Shoes", "price": 3100, "rating": 4, "image": "images/Shoes/s2.png"},
    {"name": "White Slip-On Sneakers", "price": 3200, "rating": 2, "image": "images/Shoes/s3.png"},
    {"name": "Beige Platform Sneakers", "price": 3300, "rating": 4, "image": "images/Shoes/s4.png"},
    # {"name": "Purple Casual Slip-On Shoes", "price": 3400, "rating": 2, "image": "images/Shoes/s5.png"},
    
    # Watches
    {"name": "Black Leather Strap Watch", "price": 1500, "rating": 4, "image": "images/Watch/w1.png"},
    {"name": "Sporty Black Digital Watch", "price": 1600, "rating": 3, "image": "images/Watch/w2.png"},
    {"name": "Rose Gold Analog Watch", "price": 1700, "rating": 2, "image": "images/Watch/w3.png"},
    {"name": "Silver Metal Band Watch", "price": 1800, "rating": 5, "image": "images/Watch/w4.png"},
    # {"name": "Minimalist White Dial Watch", "price": 1900, "rating": 3, "image": "images/Watch/w5.png"},
]


st.title("Clothing Store")

# Initialize cart and total price in session state
if "cart" not in st.session_state:
    st.session_state.cart = {}
    st.session_state.total_price = 0
if "budget" not in st.session_state:
    st.session_state.budget = None
    
# Optimization function: based on the knapsack problem
# Optimization function: based on the knapsack problem
def optimize_cart(cart_items, budget):
    enriched_cart_items = []
    
    # Match each cart item with clothing_items using price and enrich with ratings
    for cart_item in cart_items:
        # Find the corresponding item from clothing_items based on price and quantity
        original_item = next(
            (item for item in clothing_items if item['price'] == cart_item['price']), 
            None
        )
        
        if original_item:
            enriched_cart_items.append({
                "name": original_item['name'],  # Add name from clothing_items
                "price": cart_item['price'],
                "rating": original_item['rating'],  # Add rating from clothing_items
                "quantity": cart_item['quantity']
            })

    n = len(enriched_cart_items)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for b in range(1, budget + 1):
            if enriched_cart_items[i - 1]["price"] <= b:
                dp[i][b] = max(
                    enriched_cart_items[i - 1]["rating"] + dp[i - 1][b - enriched_cart_items[i - 1]["price"]], 
                    dp[i - 1][b]
                )
            else:
                dp[i][b] = dp[i - 1][b]
    
    # Backtrack to find selected items
    selected_items = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            selected_items.append(enriched_cart_items[i - 1])
            b -= enriched_cart_items[i - 1]["price"]
    
    return selected_items

st.sidebar.subheader("Enter your budget:")
budget_input = st.sidebar.number_input("",min_value=0, step=100)
if st.sidebar.button("Optimize Cart"):
    st.session_state.budget = budget_input

# Display optimized cart if budget is set
if st.session_state.budget is not None:
    optimized_cart = optimize_cart(list(st.session_state.cart.values()), st.session_state.budget)
    st.sidebar.subheader("Optimized Cart")
    for item in optimized_cart:
        st.sidebar.write(f"{item['name']} - ₹{item['price']} (Rating: {item['rating']})")
    optimized_total = sum(item["price"] for item in optimized_cart)
    st.sidebar.write(f"Optimized Total Price: ₹{optimized_total}")

    st.sidebar.markdown("---")
    
    # Calculate and display savings
    savings = st.session_state.budget - optimized_total
    st.sidebar.write(f"Money Saved: ₹{savings}")
    
    st.sidebar.markdown("---")    

# Function to handle updating the cart based on quantity input
def update_cart(item_name):
    updated_quantity = st.session_state[f"quantity_{item_name}"]
    
    item = next((i for i in clothing_items if i["name"] == item_name), None)
    
    if item:
        if updated_quantity > 0:
            if item_name in st.session_state.cart:
                st.session_state.total_price += (updated_quantity - st.session_state.cart[item_name]['quantity']) * item['price']
            else:
                st.session_state.total_price += item['price'] * updated_quantity
            st.session_state.cart[item_name] = {"price": item['price'], "quantity": updated_quantity}
        else:
            if item_name in st.session_state.cart:
                st.session_state.total_price -= st.session_state.cart[item_name]['price'] * st.session_state.cart[item_name]['quantity']
                del st.session_state.cart[item_name]

# Function to remove an item entirely from the cart
def remove_item(item_name):
    if item_name in st.session_state.cart:
        removed_item = st.session_state.cart[item_name]
        st.session_state.total_price -= removed_item['price'] * removed_item['quantity']
        del st.session_state.cart[item_name]
        st.session_state[f"quantity_{item_name}"] = 0  # Reset the quantity in session state

# Display the clothing items in columns (side by side)
num_cols = 3  # Number of items per row
cols = st.columns(num_cols)

for index, item in enumerate(clothing_items):
    col = cols[index % num_cols]
    with col:
        # Generate stars for the rating
        img_base64 = image_to_base64(item['image'])
        star_rating = '⭐️' * item['rating'] #+ '☆' * (5 - item['rating'])  # 5-star rating system
        # st.image(item['image'], width=370)
        # Display the item card
        st.markdown(f"""
            <div class="custom-container">
                <img src="data:image/png;base64,{img_base64}" height="230" width="200"><br>
                <h4>{item['name']}</h4>
                <p><b>Price: ₹{item['price']}</b></p>
                <h5><b>Rating: {star_rating} ({item['rating']}/5)</b></h5> <!-- Add rating here -->
            </div>
        """, unsafe_allow_html=True)

        # Initialize quantity in session state if not already set
        if f"quantity_{item['name']}" not in st.session_state:
            st.session_state[f"quantity_{item['name']}"] = 0

        # Quantity input directly linked to the cart update
        st.number_input(
            f"Quantity for {item['name']}",
            min_value=0,
            value=st.session_state[f"quantity_{item['name']}"],
            key=f"quantity_{item['name']}",
            on_change=update_cart,
            args=(item['name'],)
        )

# Display the cart in the sidebar with total price and quantity
st.sidebar.title("🛒 Shopping Cart")
st.markdown("")

if st.session_state.cart:
    for item_name, item_info in st.session_state.cart.items():
        col1, col2, col3, col4 = st.sidebar.columns([2, 1, 1, 1])
        with col1:
            st.write(f"**{item_name} (x{item_info['quantity']})**")
        with col2:
            st.write(f"₹{item_info['price']} each")
        with col3:
            st.write(f"**₹{item_info['price'] * item_info['quantity']}**")
        with col4:
            # Remove button to remove the entire item from the cart
            st.button("✖", key=f"remove_{item_name}", on_click=remove_item, args=(item_name,))

    st.sidebar.subheader(f"**Total Price: ₹{st.session_state.total_price}**")
else:
    st.sidebar.write("Your cart is empty.")
