import streamlit as st

from utils import CYLINDER_VOLUMES
from utils import DEFAULT_CYLINDER_VOLUME_INDEX
from utils import get_missing_gases_pressures

# CSS pour styliser les labels des métriques
st.html(
    """
<style>
.stMetric label p {
    font-size: 1.5rem !important;
    font-weight: bold !important;
    color: #ff4b4b !important;
}
</style>
"""
)

st.title("Gas blender")

st.subheader("Cylinder volume")

cylinder_volume = st.selectbox(
    label="Cylinder volume (L)",
    label_visibility="collapsed",
    options=CYLINDER_VOLUMES,
    index=DEFAULT_CYLINDER_VOLUME_INDEX,
    format_func=lambda x: f"{x} L",
)

st.subheader("Current mix")
with st.container(border=True, horizontal=True):
    start_pressure = st.number_input(
        label="Current pressure (in bar)",
        value=50,
        step=1,
        format="%d",
        min_value=0,
        max_value=300,
    )
    start_o2 = st.number_input(
        label="Current O2 in the mix (in %)",
        min_value=10,
        max_value=100,
        value=21,
        step=1,
    )
    start_he = st.number_input(
        label="Current He in the mix (in %)",
        min_value=0,
        max_value=70,
        value=0,
        step=1,
    )

st.subheader("Desired mix")
with st.container(border=True, horizontal=True):
    end_pressure = st.number_input(
        label="Desired pressure (in bar)",
        value=200,
        step=1,
        format="%d",
        min_value=0,
        max_value=300,
    )
    end_o2 = st.number_input(
        label="Desired O2 in the mix (in %)",
        min_value=10,
        max_value=100,
        value=21,
        step=1,
    )
    end_he = st.number_input(
        label="Desired He in the mix (in %)",
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

st.subheader("Gases to add")
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

st.subheader("Cost of the mix")
mix_price = 3.0
o2_price = 0.025
he_price = 0.08
air_price = {
    3: 3.0,
    15: 6.0,
    24: 8.0,
}

gas_number = sum(1 for value in missing.values() if value > 0)
if gas_number > 1:
    base_cost = 3.0  # Base price for mixing more than one gas
else:
    for volume, price in air_price.items():
        if cylinder_volume <= volume:
            base_cost = price
            break
o2_cost = missing["o2"] * o2_price
he_cost = missing["he"] * he_price
total_cost = base_cost + o2_cost + he_cost

with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        if gas_number > 1:
            st.metric("Mix", f"{base_cost:.2f} €", help="Base cost for multi-gas mix")
        else:
            st.metric("Air only", f"{base_cost:.2f} €", help="Air filling cost")
    with col2:
        if o2_cost > 0:
            st.metric(
                "O₂",
                f"{o2_cost:.2f} €",
                delta=f"{missing['o2']:.0f} L × {o2_price:.3f} €/L",
                help="Cost of added oxygen",
            )
        else:
            st.metric("O₂", "0.00 €", help="No oxygen added")
    with col3:
        if he_cost > 0:
            st.metric(
                "He",
                f"{he_cost:.2f} €",
                delta=f"{missing['he']:.0f} L × {he_price:.3f} €/L",
                help="Cost of added helium",
            )
        else:
            st.metric("He", "0.00 €", help="No helium added")
    st.divider()
    st.markdown(
        f"<h2 class='center'>Total: {total_cost:.2f} €</h2>",
        unsafe_allow_html=True,
    )
