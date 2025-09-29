import streamlit as st

# from db import initialize_db

# initialize_db()

st.set_page_config(page_title="Diving Tools", page_icon=":material/scuba_diving:")
st.logo(
    """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 325 55" role="img" aria-label="Logo">
        <text x="0" y="36" font-size="52" dominant-baseline="middle">🤿</text>
        <text x="75" y="30" font-size="46" font-family="Source Sans, sans-serif" font-weight="500" dominant-baseline="middle">
            Diving Tools
        </text>
    </svg>""",
    size="large",
)

streamlit_style = """
<style>
  .st-key-user_actions p {font-size: 1.2rem !important;}
  .center {text-align: center;}
  .pt-0 {padding-top: 0px !important;}
  .mt-0 {margin-top: 0px !important;}
  .pb-0 {padding-bottom: 0px !important;}
  .mb-0 {margin-bottom: 0px !important;}
  .danger {color: red !important; border: 2px solid red; padding: 0.5rem; margin: 1rem 0rem;}
  div.stMainBlockContainer {padding-top: 2rem !important;}
  hr {margin: 0px !important;}
</style>
"""
st.html(streamlit_style)

# Voir la liste des icon possibles ici : https://fonts.google.com/icons?icon.set=Material+Icons

home_page = st.Page(
    "tools/home.py",
    title="Home",
    icon=":material/home:",
)
rmv_page = st.Page(
    "tools/rmv.py",
    title="RMV",
    icon=":material/air:",
)
nitrox_page = st.Page(
    "tools/nitrox.py",
    title="Nitrox",
    icon=":material/bubble_chart:",
)
gas_planning_page = st.Page(
    "tools/planning.py",
    title="Gas planning",
    icon=":material/scuba_diving:",
)
gas_blender_page = st.Page(
    "tools/blender.py",
    title="Gas blender",
    icon=":material/auto_fix_high:",
)
preferences_page = st.Page(
    "tools/preferences.py",
    title="Preferences",
    icon=":material/person:",
)
statistics_page = st.Page(
    "tools/statistics.py",
    title="Statistics",
    icon=":material/bar_chart:",
)
# pages = [home_page, rmv_page, nitrox_page, gas_planning_page, gas_blender_page]
pages = {
    "": [home_page],
    "Tools": [rmv_page, nitrox_page, gas_planning_page, gas_blender_page],
}
if st.user.is_logged_in:
    pages["User"] = [preferences_page]
    if st.user.email == "sebastien.verbois@gmail.com":
        pages["User"].append(statistics_page)

pg = st.navigation(pages, position="sidebar")

with st.sidebar:
    if not st.user.is_logged_in:
        st.button("Login with Google", on_click=st.login, args=["google"])
    else:
        st.subheader(st.user.name)
        st.button("Logout", on_click=st.logout)

pg.run()
