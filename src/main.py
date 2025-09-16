import streamlit as st

streamlit_style = """
<style>
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
    title="Accueil",
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
gas_page = st.Page(
    "pages/gas.py",
    title="Gaz",
    icon=":material/scuba_diving:",
)
pg = st.navigation(
    [
        home_page,
        rmv_page,
        nitrox_page,
        gas_page,
    ],
    position="sidebar",
)
st.set_page_config(page_title="Diving Apps", page_icon=":material/scuba_diving:")
pg.run()
