from math import ceil

import streamlit as st

from utils import DEFAULT_PPO2_INDEX
from utils import END_DEPTHS
from utils import PPO2_VALUES, MIN_O2_IN_NORMOXIC_TRIMIX


def best_trimix(dive_depth, max_end_depth, max_ppo2):
    dive_pressure = dive_depth / 10.0 + 1.0
    max_ppn2 = (max_end_depth / 10.0 + 1.0) * 0.79
    # Get the highest O2 percentage possible
    o2_percentage = min(100, int(max_ppo2 / dive_pressure * 100))
    # Get the highest N2 percentage possible in respect of the END
    n2_percentage = min(79, 100 - o2_percentage, int(max_ppn2 / dive_pressure * 100))
    # Helium is the remainder
    he_percentage = 100 - o2_percentage - n2_percentage
    return o2_percentage, he_percentage


def end_depth(n2_percentage, dive_depth):
    dive_pressure = dive_depth / 10.0 + 1.0
    ppn2 = n2_percentage / 100.0 * dive_pressure
    ead = (ppn2 / 0.79 - 1) * 10.0
    return ceil(ead)


st.title("Trimix")
with st.expander("Description"):
    st.markdown(
        "**Trimix** is a breathing gas consisting of oxygen, nitrogen, and helium. "
        "It is used for deep diving to reduce the risks associated with nitrogen narcosis and oxygen toxicity. "
        "We use a minimal amount of oxygen of 20% to ensure normoxia and a maximum END depth of 30 m for nitrogen narcosis."
    )
with st.container(border=True):
    st.markdown("<h3 class='center'>Best Normoxic Trimix</h3>", unsafe_allow_html=True)
    l1c1, l1c2, l1c3 = st.columns(3)
    trimix_max_ppo2 = l1c1.selectbox(
        label="PPO2 max (in bar)",
        options=PPO2_VALUES,
        index=DEFAULT_PPO2_INDEX,
        format_func=lambda x: f"{x} bar",
        key="trimix_max_ppo2",
    )
    trimix_max_end_depth = l1c2.selectbox(
        label="Max END depth (in m)",
        options=END_DEPTHS,
        index=1,
        key="trimix_max_end_depth",
    )
    trimix_max_dive_depth = l1c3.slider(
        label="Max dive depth (in m)",
        min_value=40,
        max_value=int((trimix_max_ppo2 / MIN_O2_IN_NORMOXIC_TRIMIX - 1.0) * 10),
        value=45,
        step=1,
        key="trimix_max_dive_depth",
    )
    o2_percentage, he_percentage = best_trimix(trimix_max_dive_depth, trimix_max_end_depth, trimix_max_ppo2)
    n2_percentage = 100 - o2_percentage - he_percentage
    st.markdown(
        f"<div class='center'><h2>Tx {o2_percentage}/{he_percentage}</h2><h4>{o2_percentage}% O2 - {he_percentage}% He - {n2_percentage}% N2</h4></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "",
        unsafe_allow_html=True,
    )
    end_depth_value = end_depth(n2_percentage, trimix_max_dive_depth)
