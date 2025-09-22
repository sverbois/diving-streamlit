import streamlit as st

from utils import initialize_session

st.set_page_config(page_title="Diving Tools", page_icon=":material/scuba_diving:")
initialize_session()

streamlit_style = """
<style>
  .st-key-user_actions p {font-size: 1.2rem !important;}
  .center {text-align: center;}
  .mt-0 {margin-top: 0px;}
  .danger {color: red !important; border: 2px solid red; padding: 0.5rem; margin: 1rem 0rem;}
  div.stMainBlockContainer {padding-top: 1rem !important;}
  hr {margin: 0px !important;}
</style>
"""
st.markdown(streamlit_style, unsafe_allow_html=True)

# Voir la liste des icon possibles ici : https://fonts.google.com/icons?icon.set=Material+Icons

home_page = st.Page(
    "pages/home.py",
    title="Home",
    icon=":material/home:",
)
rmv_page = st.Page(
    "pages/rmv.py",
    title="RMV",
    icon=":material/air:",
)
nitrox_page = st.Page(
    "pages/nitrox.py",
    title="Nitrox",
    icon=":material/bubble_chart:",
)
gas_planning_page = st.Page(
    "pages/planning.py",
    title="Gas planning",
    icon=":material/scuba_diving:",
)
gas_blender_page = st.Page(
    "pages/blender.py",
    title="Gas blender",
    icon=":material/auto_fix_high:",
)
preferences_page = st.Page(
    "pages/preferences.py",
    title="Preferences",
    icon=":material/person:",
)
statistics_page = st.Page(
    "pages/statistics.py",
    title="Statistics",
    icon=":material/bar_chart:",
)
pages = [home_page, rmv_page, nitrox_page, gas_planning_page, gas_blender_page]
if st.user.is_logged_in:
    pages.append(preferences_page)
    if st.user.email == "sebastien.verbois@gmail.com":
        pages.append(statistics_page)

pg = st.navigation(pages, position="sidebar")

with st.sidebar:
    if not st.user.is_logged_in:
        st.button("Login with Google", on_click=st.login, args=["google"])
    else:
        action = st.selectbox(
            label=f"**{st.user.name}**",
            options=("Preferences", "Logout"),
            index=None,
            placeholder="Actions…",
            key="user_actions",
        )
        if action == "Logout":
            st.logout()
        elif action == "Preferences":
            st.switch_page(preferences_page)
            st.rerun()

pg.run()
