import math

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import CYLINDER_VOLUMES
from utils import DEFAULT_CYLINDER_VOLUME_INDEX
from utils import get_user_data

USER_DATA = get_user_data()

ASCENT_SPEED = 10  # m/min
DESCENT_SPEED = 20  # m/min
DECO_DEPTH = 6  # m
SAFETY_STOP_DURATION = 5  # min
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
    rmv = col1.slider("RMV (L/min)", min_value=8, max_value=25, value=USER_DATA.rmv, step=1)
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


def add_ascent_and_descent_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.reset_index(drop=True)  # Reset index to ensure proper iteration
    df.loc[len(df)] = {"depth": DECO_DEPTH, "duration": SAFETY_STOP_DURATION + decompression_time}
    first = pd.DataFrame([{"depth": 0, "duration": 0}])
    df = pd.concat([first, df], ignore_index=True)
    rows: list[dict] = []
    for i in range(len(df)):
        level = df.iloc[i]
        # Ajoute le niveau
        rows.append(
            {
                "depth": level["depth"],
                "duration": level["duration"],
                "type": "constant" if i < len(df) - 1 else "deco",
            }
        )
        # Insère la descente / remontée
        if i < len(df) - 1:
            next_depth = df.iloc[i + 1]["depth"]
            avg_depth = (level["depth"] + next_depth) / 2
            diff_depth = next_depth - level["depth"]
            rows.append(
                {
                    "depth": avg_depth,
                    "duration": diff_depth / DESCENT_SPEED if diff_depth > 0 else abs(diff_depth) / ASCENT_SPEED,
                    "type": "descent" if diff_depth > 0 else "ascent",
                }
            )
            rows[0]["type"] = "start"
        if rows[-1]["type"] == "deco":
            rows.append(
                {
                    "depth": 0,
                    "duration": rows[-1]["depth"] / ASCENT_SPEED,
                    "type": "ascent",
                }
            )
    return pd.DataFrame(rows)


# Nouveau DataFrame avec profondeurs de descente/remontée
fulldata = add_ascent_and_descent_data(
    data,
)

pressures = 1 + fulldata["depth"] / 10
fulldata["consumption"] = pressures * rmv * fulldata["duration"]
fulldata["icon"] = fulldata["type"].map(ICONS)
fulldata["runtime"] = fulldata["duration"].cumsum()
fulldata["pressure"] = cylinder_pressure - (fulldata["consumption"].cumsum() / cylinder_volume)
# Arrondir les durées à l'entier supérieur pour l'affichage
fulldata["duration_display"] = fulldata["duration"].apply(math.ceil)
# Masque la profondeur pour les segments de montée / descente dans l'affichage final
fulldata["depth_display"] = fulldata.apply(
    lambda r: "⬆️" if r["type"] == "ascent" else "⬇️" if r["type"] == "descent" else f"{int(r['depth'])} m",
    axis=1,
)

st.dataframe(
    fulldata,
    hide_index=True,
    column_order=["depth_display", "duration_display", "consumption", "runtime", "pressure"],
    column_config=COLUMN_CONFIG,
)

total_consumption_in_l = int(fulldata["consumption"].sum())
total_consumption_in_bar = total_consumption_in_l / cylinder_volume
reserve_in_bar = int(cylinder_pressure - total_consumption_in_bar)
total_time_in_min = int(fulldata["duration"].sum())

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

partialdata = fulldata[["depth", "runtime", "type"]]
for i in range(len(partialdata)):
    if partialdata.iloc[i]["type"] in ["ascent", "descent"]:
        # Si ce n'est pas la dernière ligne, utilise la profondeur de la ligne suivante
        if i + 1 < len(partialdata):
            partialdata.iloc[i, partialdata.columns.get_loc("depth")] = partialdata.iloc[i + 1]["depth"]

fig = px.line(
    partialdata,
    x="runtime",
    y="depth",
    # title="Diving profile",
    labels={"runtime": "Runtime (min)", "depth": "Depth (m)"},
)
fig.update_yaxes(autorange="reversed")

plotly_config = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["zoom", "zoomin", "zoomout", "autoscale", "resetscale", "pan"],
}
st.plotly_chart(fig, use_container_width=True, config=plotly_config)
