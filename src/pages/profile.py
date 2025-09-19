import streamlit as st
import streamlit_pydantic as sp

from utils import initialize_session
from utils import save_user_data

initialize_session()
user_data = st.session_state["user_data"]

st.title("Profile")
st.markdown(f"#### {st.user.email}")

profile1, profile2 = st.tabs(["Préférences 1", "Préférences 2"])

with profile1:
    data = sp.pydantic_form(key="user_form", model=user_data, submit_label="Enregistrer mon profil")
    if data:
        save_user_data(data)
        st.toast("Profil enregistré avec succès !", icon="✅")

with profile2:
    st.write("Contenu des préférences 2")
