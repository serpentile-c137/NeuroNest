import streamlit as st
from db import add_user, login_user

def show_login():
    st.title("🔐 NeuroNest Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.session_state["user"] = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

def show_signup():
    st.title("🧾 Register for NeuroNest")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Create Account"):
        try:
            add_user(username, password)
            st.success("Account created! Please log in.")
        except:
            st.error("Username already exists")
