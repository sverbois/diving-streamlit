import streamlit as st

from utils import DEFAULT_PPO2_INDEX
from utils import PPO2_VALUES


def compute_mod(ppo2_max, o2_percentage):
    if not (ppo2_max and o2_percentage):
        return 0.0
    max_pressure_in_bar = ppo2_max / (o2_percentage / 100.0)
    mod_in_m = (max_pressure_in_bar - 1.0) * 10.0
    return int(mod_in_m)


def best_mix(ppo2_max, depth):
    if not (ppo2_max and depth):
        return 0
    depth_in_bar = depth / 10.0 + 1.0
    return min(100, int(ppo2_max / depth_in_bar * 100))


def equivalent_air_depth(o2_percentage, nitrox_depth):
    if not (o2_percentage and nitrox_depth):
        return 0.0
    n2_percentage = 100 - o2_percentage
    pabs = nitrox_depth / 10.0 + 1
    ppn2 = n2_percentage / 100.0 * pabs
    ead = (ppn2 / 0.79 - 1) * 10.0
    return int(ead)


st.title("Nitrox")
with st.expander("Description"):
    st.markdown(
        "**Nitrox** is an oxygen-enriched mixture. It contains as little as 40% oxygen for a bottom gas and up to 100% for a decompression gas."
    )
with st.container(border=True):
    st.markdown("<h3 class='center'>Maximum operating depth (MOD)</h3>", unsafe_allow_html=True)
    l1c1, l1c2 = st.columns(2)
    mod_ppo2_max = l1c1.selectbox(
        label="PPO2 max (in bar)",
        options=PPO2_VALUES,
        index=DEFAULT_PPO2_INDEX,
        format_func=lambda x: f"{x} bar",
        key="mod_ppo2_max",
    )
    mod_o2_max = l1c2.slider(
        label="O2 in Nitrox (in %)",
        min_value=21,
        max_value=100,
        value=40,
        step=1,
        key="mod_o2_max",
    )
    st.markdown(
        f"<h2 class='center'>{compute_mod(mod_ppo2_max, mod_o2_max)} m</h2>",
        unsafe_allow_html=True,
    )

with st.container(border=True):
    st.markdown("<h3 class='center'>Best Nitrox</h3>", unsafe_allow_html=True)
    l2c1, l2c2 = st.columns(2)
    best_ppo2_max = l2c1.selectbox(
        label="PPO2 max (in bar)",
        options=PPO2_VALUES,
        index=DEFAULT_PPO2_INDEX,
        format_func=lambda x: f"{x} bar",
        key="best_ppo2_max",
    )
    best_max_depth = l2c2.slider(
        label="Maximum depth (in m)",
        min_value=15,
        max_value=68,
        value=30,
        step=1,
        key="best_max_depth",
    )
    st.markdown(f"<h2 class='center'>{best_mix(best_ppo2_max, best_max_depth)} % O2</h2>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("<h3 class='center'>Equivalent air depth (EAD)</h3>", unsafe_allow_html=True)
    l3c1, l3c2 = st.columns(2)
    o2percentage = l3c1.slider(
        label="O2 in Nitrox (in %)",
        min_value=21,
        max_value=40,
        value=21,
        step=1,
        key="o2percentage",
    )
    depth = l3c2.slider(
        label="Depth (in m)",
        min_value=20,
        max_value=68,
        value=30,
        step=1,
        key="depth",
    )
    st.markdown(f"<h2 class='center'>{equivalent_air_depth(o2percentage, depth)} m</h2>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("<h3 class='center'>Partial pressure O2 (PP02)</h3>", unsafe_allow_html=True)
    st.write("TODO")
