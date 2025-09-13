import streamlit as st


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
with st.expander("Définition"):
    st.markdown(
        "Le **Nitrox** est un mélange enrichi en oxygène. Il contient juste qu'à 40% d'oxygène pour un gaz de fond et jusqu'à 100% pour un gaz de déco."
    )
with st.container(border=True):
    st.markdown("<h3 class='center'>Profondeur maximale d'utilisation (MOD)</h3>", unsafe_allow_html=True)
    l1c1, l1c2 = st.columns(2)
    mod_ppo2_max = l1c1.selectbox(
        label="PPO2 max (en bar)",
        options=(1.3, 1.4, 1.5, 1.6),
        index=3,
        format_func=lambda x: f"{x} bar",
        key="mod_ppo2_max",
    )
    mod_o2_max = l1c2.slider(
        label="O2 dans le Nitrox (en %)",
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
    st.markdown("<h3 class='center'>Meilleur Nitrox</h3>", unsafe_allow_html=True)
    l2c1, l2c2 = st.columns(2)
    best_ppo2_max = l2c1.selectbox(
        label="PPO2 max (en bar)",
        options=(1.3, 1.4, 1.5, 1.6),
        index=3,
        format_func=lambda x: f"{x} bar",
        key="best_ppo2_max",
    )
    best_max_depth = l2c2.slider(
        label="Profondeur max (en m)",
        min_value=15,
        max_value=68,
        value=30,
        step=1,
        key="best_max_depth",
    )
    st.markdown(f"<h2 class='center'>{best_mix(best_ppo2_max, best_max_depth)} % O2</h2>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("<h3 class='center'>Profondeur équivalente à l'air (EAD)</h3>", unsafe_allow_html=True)
    l3c1, l3c2 = st.columns(2)
    o2percentage = l3c1.slider(
        label="O2 dans le Nitrox (en %)",
        min_value=21,
        max_value=40,
        value=21,
        step=1,
        key="o2percentage",
    )
    depth = l3c2.slider(
        label="Profondeur (en m)",
        min_value=20,
        max_value=68,
        value=30,
        step=1,
        key="depth",
    )
    st.markdown(f"<h2 class='center'>{equivalent_air_depth(o2percentage, depth)} m</h2>", unsafe_allow_html=True)

streamlit_style = """
    <style>
        .center {
            text-align: center;
        }
        .mt-0 {
            margin-top: 0px;
        }
    </style>
"""
st.markdown(streamlit_style, unsafe_allow_html=True)
