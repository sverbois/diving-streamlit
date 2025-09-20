import streamlit as st

from utils import get_missing_gases_pressures

# CSS pour styliser les labels des métriques
st.markdown(
    """
<style>
.stMetric label p {
    font-size: 1.5rem !important;
    font-weight: bold !important;
    color: #ff4b4b !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("Gas blender")

st.subheader("Volume de la bouteille")

cylinder_volume = st.selectbox(
    label="Volume bouteille (L)",
    label_visibility="collapsed",
    options=(10, 12, 15, 16, 20, 24),
    index=2,
    format_func=lambda x: f"{x} L",
)

st.subheader("Mélange actuel")
with st.container(border=True, horizontal=True):
    start_pressure = st.number_input(
        label="Pression actuelle (en bars)",
        value=50,
        step=1,
        format="%d",
        min_value=0,
        max_value=300,
    )
    start_o2 = st.number_input(
        label="O2 actuel dans le mélange (en %)",
        min_value=10,
        max_value=100,
        value=21,
        step=1,
    )
    start_he = st.number_input(
        label="He actuel dans le mélange (en %)",
        min_value=0,
        max_value=70,
        value=0,
        step=1,
    )

st.subheader("Mélange désiré")
with st.container(border=True, horizontal=True):
    end_pressure = st.number_input(
        label="Pression désirée (en bars)",
        value=200,
        step=1,
        format="%d",
        min_value=0,
        max_value=300,
    )
    end_o2 = st.number_input(
        label="O2 désiré dans le mélange (en %)",
        min_value=10,
        max_value=100,
        value=21,
        step=1,
    )
    end_he = st.number_input(
        label="He désiré dans le mélange (en %)",
        min_value=0,
        max_value=70,
        value=0,
        step=1,
    )

missing = get_missing_gases_pressures(
    cylinder_volume=cylinder_volume,
    start_pressure=start_pressure,
    end_pressure=end_pressure,
    start_he_percentage=start_he,
    end_he_percentage=end_he,
    start_o2_percentage=start_o2,
    end_o2_percentage=end_o2,
)
ps = {
    "start": start_pressure,
    "o2": missing["o2"] / cylinder_volume,
    "he": missing["he"] / cylinder_volume,
    "air": missing["air"] / cylinder_volume,
}

st.subheader("Gaz à ajouter")
g1, g2 = st.columns(2, border=True)
with g1:
    st.markdown("#### O2 → He → Air")
    if ps["o2"] > 0:
        st.metric(
            "O2",
            f"{ps['start']:.0f} bar → {ps['start'] + ps['o2']:.0f} bar",
            delta=f"+ {int(missing['o2'])} L",
            border=True,
        )
    if ps["he"] > 0:
        st.metric(
            "He",
            f"{ps['start'] + ps['o2']:.0f} bar → {ps['start'] + ps['o2'] + ps['he']:.0f} bar",
            delta=f"+ {int(missing['he'])} L",
            border=True,
        )
    if ps["air"] > 0:
        st.metric(
            "Air",
            f"{ps['start'] + ps['o2'] + ps['he']:.0f} bar → {ps['start'] + ps['o2'] + ps['he'] + ps['air']:.0f} bar",
            delta=f"+ {int(missing['air'])} L",
            border=True,
        )
with g2:
    st.markdown("#### He → O2 → Air")
    if ps["he"] > 0:
        st.metric(
            "He",
            f"{ps['start']:.0f} bar → {ps['start'] + ps['he']:.0f} bar",
            delta=f"+ {int(missing['he'])} L",
            border=True,
        )
    if ps["o2"] > 0:
        st.metric(
            "O2",
            f"{ps['start'] + ps['he']:.0f} bar → {ps['start'] + ps['he'] + ps['o2']:.0f} bar",
            delta=f"+ {int(missing['o2'])} L",
            border=True,
        )
    if ps["air"] > 0:
        st.metric(
            "Air",
            f"{ps['start'] + ps['he'] + ps['o2']:.0f} bar → {ps['start'] + ps['he'] + ps['o2'] + ps['air']:.0f} bar",
            delta=f"+ {int(missing['air'])} L",
            border=True,
        )

st.subheader("Coût du mélange")
st.write("TODO")
