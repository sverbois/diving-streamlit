import streamlit as st

st.title("Statistics")

st.subheader("Users in database")
conn = st.connection("sqlite", type="sql")
users = conn.query("SELECT email,data FROM users", ttl=0)
st.dataframe(users)
