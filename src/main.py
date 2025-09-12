import streamlit as st

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
    ]
)
pg.run()
