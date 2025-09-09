import streamlit as st


def compute_rmv(cylinder_volume, start_pressure, end_pressure, dive_time, mean_depth):
    if not (cylinder_volume and start_pressure and end_pressure and dive_time and mean_depth):
        return 0.0
    pressure = mean_depth / 10.0 + 1.0
    return (cylinder_volume * (start_pressure - end_pressure)) / (dive_time * pressure)


st.title("Calcul du RMV")
st.markdown(
    "Le **RMV** (Respiratory Minute Volume) est la quantité d'air ou de gaz respiré par un plongeur en une minute. Il est exprimé en litres par minute (L/min)."
)
st.divider()
cylinder_volume = st.radio(
    label="Volume bouteille (en litres)",
    options=(10, 12, 15, 16, 20, 24),
    index=2,
    horizontal=True,
    format_func=lambda x: f"{x} L",
)
left, right = st.columns(2, vertical_alignment="bottom")
start_pressure = left.number_input(
    label="Pression début plongée (en bars)",
    value=200,
    step=10,
    format="%d",
    min_value=50,
    max_value=300,
)
end_pressure = right.number_input(
    label="Pression fin plongée (en bars)",
    value=50,
    step=10,
    format="%d",
    min_value=10,
    max_value=start_pressure - 10,
)
dive_time = left.number_input(
    label="Durée plongée (en minutes)",
    value=45,
    step=1,
    format="%d",
    min_value=10,
    max_value=120,
)
mean_depth = right.number_input(
    label="Profondeur moyenne (en mètres)",
    value=15.0,
    step=0.5,
    format="%0.1f",
    min_value=10.0,
    max_value=30.0,
)
st.divider()
rmv = compute_rmv(cylinder_volume, start_pressure, end_pressure, dive_time, mean_depth)
st.markdown(f"<h5 style='text-align:center;'>Votre RMV est de {rmv:.1f} L/min</h5>", unsafe_allow_html=True)

### Remove Streamlit header and footer
hide_streamlit_header_footer = """
    <style>
    header {display: none !important;}
    a {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_header_footer, unsafe_allow_html=True)
