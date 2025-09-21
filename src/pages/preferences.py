import streamlit as st
import streamlit_pydantic as sp

from utils import get_user_data
from utils import save_user_data

USER_DATA = get_user_data()

st.title("Preferences")
with st.expander("Description"):
    st.markdown("This page allow you to set preferences that will be used as default values in the different tools.")
st.subheader(st.user.email)

profile1, profile2 = st.tabs(["Diving preferences", "Blender prices"])

with profile1:
    data = sp.pydantic_form(key="user_form", model=USER_DATA, submit_label="Save my profile")
    if data:
        save_user_data(data)
        st.toast("Profile saved successfully!", icon="✅")

with profile2:
    st.write("TODO")
