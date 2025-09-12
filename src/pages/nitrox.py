import streamlit as st


def compute_mod(ppo2_max, o2_percentage):
    if not (ppo2_max and o2_percentage):
        return 0.0
    mod = (ppo2_max / (o2_percentage / 100.0) - 1.0) * 10.0
    return int(mod)


def best_mix(ppo2_max, depth):
    if not (ppo2_max and depth):
        return 0
    return min(100, int(ppo2_max / (depth / 10.0 + 1.0) * 100))


st.title("Meilleure mélange Nitrox")
with st.expander("Définition"):
    st.markdown(
        "Le **Nitrox** est un mélange enrichi en oxygène. Il contient juste qu'à 40% d'oxygène pour un gaz de fond et jusqu'à 100% pour un gaz de déco."
    )
st.divider()

pc1, pc2, pc3 = st.columns(3, vertical_alignment="bottom")
ppo2_max = pc1.selectbox(
    label="PPO2 max (en bar)",
    options=(1.3, 1.4, 1.5, 1.6, 2.0),
    index=3,
    format_func=lambda x: f"{x} bar",
)
st.divider()
with st.container(border=True, horizontal=True, vertical_alignment="center", gap="large"):
    o2_percentage = st.slider(label="O2 dans le mélange (en %)", min_value=21, max_value=100, value=40, step=1)
    st.markdown(f"#### MOD = {compute_mod(ppo2_max, o2_percentage)} m")

with st.container(border=True, horizontal=True, vertical_alignment="center", gap="large"):
    depth = st.slider(label="Profondeur (en m)", min_value=6, max_value=68, value=40, step=1)
    st.markdown(f"#### Meilleur mélange = **{best_mix(ppo2_max, depth)} % O2**")
