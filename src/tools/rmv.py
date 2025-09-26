import streamlit as st

from utils import CYLINDER_VOLUMES
from utils import DEFAULT_CYLINDER_VOLUME_INDEX


def compute_rmv(cylinder_volume, start_pressure, end_pressure, dive_time, mean_depth):
    if not (cylinder_volume and start_pressure and end_pressure and dive_time and mean_depth):
        return 0.0
    pressure = mean_depth / 10.0 + 1.0
    return (cylinder_volume * (start_pressure - end_pressure)) / (dive_time * pressure)


st.title("RMV")
with st.expander("Description"):
    st.markdown(
        "RMV (Respiratory Minute Volume) is the amount of air or gas breathed by a diver in one minute. "
        "It is expressed in liters per minute (L/min). "
        "Knowing your RMV allows you to better plan your dives and manage your gas consumption."
    )

cylinder_volume = st.radio(
    label="Cylinder volume (in liters)",
    options=CYLINDER_VOLUMES,
    index=DEFAULT_CYLINDER_VOLUME_INDEX,
    horizontal=True,
    format_func=lambda x: f"{x} L",
)
left, right = st.columns(2, vertical_alignment="bottom")
start_pressure = left.number_input(
    label="Starting pressure (in bars)",
    value=200,
    step=10,
    format="%d",
    min_value=50,
    max_value=300,
)
end_pressure = left.number_input(
    label="Ending pressure (in bars)",
    value=50,
    step=10,
    format="%d",
    min_value=10,
    max_value=start_pressure - 10,
)
dive_time = right.number_input(
    label="Dive time (in minutes)",
    value=45,
    step=1,
    format="%d",
    min_value=10,
    max_value=120,
)
mean_depth = right.number_input(
    label="Mean depth (in meters)",
    value=15.0,
    step=0.5,
    format="%0.1f",
    min_value=10.0,
    max_value=30.0,
)
st.divider()
rmv = compute_rmv(cylinder_volume, start_pressure, end_pressure, dive_time, mean_depth)
st.markdown(f"<h3 class='center'>Your RMV is {rmv:.1f} L/min</h3>", unsafe_allow_html=True)
