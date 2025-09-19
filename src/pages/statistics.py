import streamlit as st

from utils import initialize_session

initialize_session()
user_data = st.session_state["user_data"]

st.title("Statistics")

st.subheader("Users in database")
conn = st.connection("sqlite", type="sql")
users = conn.query("SELECT email,data FROM users", ttl=0)
st.dataframe(users)
