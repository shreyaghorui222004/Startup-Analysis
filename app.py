import streamlit as st
import streamlit_authenticator as stauth
import json
import os
import bcrypt

# ----------------------------
# Load user database from file
# ----------------------------
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)

# ----------------------------
# Register new user
# ----------------------------
def register_user(email, name, password):
    users = load_users()
    if email in users:
        return False  # User already exists
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[email] = {"name": name, "password": hashed_pw}
    save_users(users)
    return True

# ----------------------------
# Authenticate user
# ----------------------------
def authenticate_user(email, password):
    users = load_users()
    user = users.get(email)
    if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
        return user["name"]
    return None

# ----------------------------
# Streamlit App
# ----------------------------
st.set_page_config(page_title="Login App", layout="centered")

# Sidebar navigation
page = st.sidebar.selectbox("Navigate", ["Login", "Register"])

if page == "Register":
    st.title("🔐 Register")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        if name and email and password:
            success = register_user(email, name, password)
            if success:
                st.success("Registration successful! You can now login.")
            else:
                st.error("User already exists.")
        else:
            st.warning("Please fill all fields.")

elif page == "Login":
    st.title("🔑 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_name = authenticate_user(email, password)
        if user_name:
            st.success(f"Welcome {user_name}! 👋")
            st.session_state["logged_in"] = True
            st.session_state["user_name"] = user_name
        else:
            st.error("Invalid credentials.")

# ----------------------------
# Dashboard (if logged in)
# ----------------------------
if st.session_state.get("logged_in"):
    st.title("📊 Dashboard")
    st.write(f"Hello, **{st.session_state['user_name']}** 👋")
    st.write("Welcome to your dashboard!")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Visitors Today", "1,204", "+5%")
    with col2:
        st.metric("Tasks Completed", "78", "+12%")

    st.button("Logout", on_click=lambda: st.session_state.clear())

