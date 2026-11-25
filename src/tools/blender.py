import streamlit as st

from config import AIR_PRICES
from config import CYLINDER_VOLUMES
from config import DEFAULT_CYLINDER_VOLUME_INDEX
from config import HE_PRICE
from config import MIX_PRICE
from config import O2_PRICE
from utils import filling_base_cost
from utils import get_missing_gases

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

GAS_LABELS = {"o2": "O2", "he": "He", "air": "Air"}

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

if start_o2 + start_he > 100 or end_o2 + end_he > 100:
    st.error("O2 and He cannot add up to more than 100% of a mix.")
    st.stop()

missing = get_missing_gases(
    cylinder_volume=cylinder_volume,
    start_pressure=start_pressure,
    end_pressure=end_pressure,
    start_he_percentage=start_he,
    end_he_percentage=end_he,
    start_o2_percentage=start_o2,
    end_o2_percentage=end_o2,
)
if any(round(volume) < 0 for volume in missing.values()):
    st.error("This mix cannot be reached by only adding gas: the cylinder must be partly emptied first.")
    st.stop()

st.subheader("Gases to add")
for column, order in zip(st.columns(2, border=True), (("o2", "he", "air"), ("he", "o2", "air"))):
    with column:
        st.markdown("#### " + " → ".join(GAS_LABELS[gas] for gas in order))
        pressure = start_pressure
        for gas in order:
            added_pressure = missing[gas] / cylinder_volume
            if added_pressure > 0:
                st.metric(
                    GAS_LABELS[gas],
                    f"{pressure:.0f} bar → {pressure + added_pressure:.0f} bar",
                    delta=f"+ {round(missing[gas])} L",
                    border=True,
                )
            pressure += added_pressure

st.subheader("Cost of the mix")
gas_number = sum(1 for value in missing.values() if value > 0)
base_cost = filling_base_cost(missing, cylinder_volume, MIX_PRICE, AIR_PRICES)
o2_cost = missing["o2"] * O2_PRICE
he_cost = missing["he"] * HE_PRICE
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
                delta=f"{missing['o2']:.0f} L × {O2_PRICE:.3f} €/L",
                help="Cost of added oxygen",
            )
        else:
            st.metric("O₂", "0.00 €", help="No oxygen added")
    with col3:
        if he_cost > 0:
            st.metric(
                "He",
                f"{he_cost:.2f} €",
                delta=f"{missing['he']:.0f} L × {HE_PRICE:.3f} €/L",
                help="Cost of added helium",
            )
        else:
            st.metric("He", "0.00 €", help="No helium added")
    st.divider()
    st.markdown(
        f"<h2 class='center'>Total: {total_cost:.2f} €</h2>",
        unsafe_allow_html=True,
    )
