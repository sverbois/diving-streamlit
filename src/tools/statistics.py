import streamlit as st

from db import get_users

st.title("Statistics")

st.subheader("Users in database")
st.dataframe(get_users())
