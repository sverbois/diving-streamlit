import streamlit as st

from db import UserPreferences
from db import save_preferences

PREFERENCES = st.session_state["preferences"]

st.title("Preferences")
with st.expander("Description"):
    st.markdown("This page allow you to set preferences that will be used as default values in the different tools.")
st.header(st.user.name)

profile1, profile2 = st.tabs(["Diving preferences", "Blender prices"])

with profile1:
    with st.form("user_form"):
        rmv = st.number_input("RMV in L/min", min_value=1, value=PREFERENCES.rmv)
        descent_speed = st.number_input("Descent speed in m/min", min_value=1, value=PREFERENCES.descent_speed)
        submitted = st.form_submit_button("Save my profile", icon=":material/save:")
    if submitted:
        preferences = UserPreferences(rmv=rmv, descent_speed=descent_speed)
        save_preferences(st.user.email, preferences)
        st.session_state["preferences"] = preferences
        st.toast("Profile saved successfully!", icon=":material/check_circle:")

with profile2:
    st.write("TODO")
