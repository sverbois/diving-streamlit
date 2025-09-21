import streamlit as st
import streamlit_pydantic as sp

from utils import get_user_data
from utils import save_user_data

USER_DATA = get_user_data()

st.title("Profile")
st.markdown(f"#### {st.user.email}")

profile1, profile2 = st.tabs(["Preferences 1", "Preferences 2"])

with profile1:
    data = sp.pydantic_form(key="user_form", model=USER_DATA, submit_label="Save my profile")
    if data:
        save_user_data(data)
        st.toast("Profile saved successfully!", icon="✅")

with profile2:
    st.write("TODO")
