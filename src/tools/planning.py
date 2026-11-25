import math

import pandas as pd
import plotly.express as px
import streamlit as st

from config import ASCENT_SPEED
from config import CYLINDER_VOLUMES
from config import DECO_DEPTH
from config import DEFAULT_CYLINDER_VOLUME_INDEX
from config import SAFETY_STOP_DURATION
from utils import add_gas_consumption
from utils import build_dive_profile

PREFERENCES = st.session_state["preferences"]

COLUMN_CONFIG = {
    "icon": st.column_config.TextColumn(
        "",
        width=30,
    ),
    "depth": st.column_config.NumberColumn(
        "Depth (m)",
        min_value=10,
        max_value=68,
        step=1,
        format="%d m",
        required=True,
    ),
    # Colonne d'affichage (texte) pour masquer la profondeur pendant les phases de montée/descente
    "depth_display": st.column_config.TextColumn(
        "Depth (m)",
    ),
    "duration": st.column_config.NumberColumn(
        "Duration (min)",
        min_value=1,
        max_value=90,
        step=1,
        format="%d min",
        required=True,
    ),
    "duration_display": st.column_config.NumberColumn(
        "Duration (min)",
        format="%d min",
    ),
    "consumption": st.column_config.NumberColumn(
        "Consumption (L)",
        format="%d L",
    ),
    "runtime": st.column_config.NumberColumn(
        "Runtime (min)",
        format="%d min",
    ),
    "pressure": st.column_config.NumberColumn(
        "Pressure (bar)",
        format="%d bar",
    ),
}
ICONS = {
    "start": "🚀",
    "constant": "🤿",
    "ascent": "⬆️",
    "descent": "⬇️",
    "deco": "🫧",
}


st.title("Gas planning")
with st.expander("Description"):
    st.markdown(
        "This form calculates gas consumption during a multi-level dive. "
        "It is assumed that the stops are made at an average depth of 6 m with a safety stop of 5 minutes."
    )
with st.container(border=True):
    col1, col2 = st.columns(2)
    rmv = col1.slider(
        "RMV (L/min)",
        min_value=8,
        max_value=25,
        value=PREFERENCES.rmv,
        step=1,
    )
    descent_speed = col1.slider(
        "Descent speed (m/min)",
        min_value=10,
        max_value=30,
        value=PREFERENCES.descent_speed,
        step=2,
    )
    cylinder_volume = col1.selectbox(
        label="Cylinder volume (L)",
        options=CYLINDER_VOLUMES,
        index=DEFAULT_CYLINDER_VOLUME_INDEX,
        format_func=lambda x: f"{x} L",
    )
    cylinder_pressure = col1.slider("Cylinder pressure (bar)", min_value=50, max_value=300, value=200, step=10)
    col2.text("Dive parameters")
    data_default = pd.DataFrame([{"depth": 40, "duration": 5}, {"depth": 20, "duration": 10}])
    data = col2.data_editor(
        data_default, num_rows="dynamic", column_order=["depth", "duration"], column_config=COLUMN_CONFIG
    )
    decompression_time = col2.slider("Decompression time (min)", min_value=0, max_value=20, value=0, step=1)

profile = build_dive_profile(
    data,
    descent_speed=descent_speed,
    ascent_speed=ASCENT_SPEED,
    stop_depth=DECO_DEPTH,
    stop_duration=SAFETY_STOP_DURATION + decompression_time,
)
fulldata = add_gas_consumption(profile, rmv=rmv, cylinder_volume=cylinder_volume, cylinder_pressure=cylinder_pressure)
fulldata["icon"] = fulldata["type"].map(ICONS)
# Arrondir les durées à l'entier supérieur pour l'affichage
fulldata["duration_display"] = fulldata["duration"].apply(math.ceil)
# Masque la profondeur pour les segments de montée / descente dans l'affichage final
fulldata["depth_display"] = fulldata.apply(
    lambda r: "⬆️" if r["type"] == "ascent" else "⬇️" if r["type"] == "descent" else f"{round(r['depth'])} m",
    axis=1,
)

st.dataframe(
    fulldata,
    hide_index=True,
    column_order=["depth_display", "duration_display", "consumption", "runtime", "pressure"],
    column_config=COLUMN_CONFIG,
)

total_consumption_in_l = round(fulldata["consumption"].sum())
total_consumption_in_bar = total_consumption_in_l / cylinder_volume
reserve_in_bar = round(cylinder_pressure - total_consumption_in_bar)
total_time_in_min = round(fulldata["duration"].sum())

if reserve_in_bar < 50:
    st.markdown(
        "<div class='center danger'><h3>DANGER !</h3><h5>Your reserve is insufficient !</h5></div>",
        unsafe_allow_html=True,
    )
with st.container(horizontal=True):
    st.metric(
        label="Total time (min)",
        value=f"{total_time_in_min} min",
        border=True,
    )
    st.metric(
        label="Consumption (L)",
        value=f"{total_consumption_in_l} L",
        border=True,
    )
    st.metric(
        label="Reserve (bar)",
        value=f"{reserve_in_bar} bar",
        border=True,
    )

fig = px.line(
    fulldata,
    x="runtime",
    y="end_depth",
    # title="Diving profile",
    labels={"runtime": "Runtime (min)", "end_depth": "Depth (m)"},
)
fig.update_yaxes(autorange="reversed")

plotly_config = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["zoom", "zoomin", "zoomout", "autoscale", "resetscale", "pan"],
}
st.plotly_chart(fig, width="stretch", config=plotly_config)
