from time import sleep

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.title("Compartment Half-Life")
with st.expander("Description"):
    st.markdown(
        "In scuba diving, a compartment half-life is the time it takes for a tissue to absorb or release half of the difference in nitrogen pressure compared to the surrounding pressure. "
        "Each tissue compartment is modeled with its own half-life, ranging from fast (minutes) to slow (hours). "
        "These half-lives are used in decompression models to predict safe ascent profiles and avoid decompression sickness."
    )

st.write("TODO: faire une animation pour une SEULE plongée et une pour plusieurs plongées")
data = pd.DataFrame(
    {
        "halflife": [
            4.0,
            8.0,
            12.5,
            18.5,
            27.0,
            38.3,
            54.3,
            77.0,
            109.0,
            146.0,
            187.0,
            239.0,
            305.0,
            390.0,
            498.0,
            635.0,
        ],
        "saturation": [0] * 16,
    }
)
data["Half-Life"] = data["halflife"].astype(str) + " min"
data["sursaturation"] = [0] * 16
data["remaining"] = 100 - (data["sursaturation"])


def increase_saturation(data, hours=1):
    time = hours * 60
    data["remaining"] = data["remaining"] * (0.5 ** (time / data["halflife"]))
    data["sursaturation"] = 100 - data["remaining"]


def decrease_saturation(data, hours=1):
    time = hours * 60
    data["sursaturation"] = data["sursaturation"] * (0.5 ** (time / data["halflife"]))
    data["remaining"] = 100 - data["sursaturation"]


def draw_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data["Half-Life"], y=data["sursaturation"], name="Sursaturation", marker_color="blue"))
    fig.add_trace(go.Bar(x=data["Half-Life"], y=data["remaining"], name="Remaining", marker_color="lightgrey"))
    fig.update_layout(barmode="stack")
    st.plotly_chart(fig, width="stretch")


slot = st.empty()


def increase_with_sleep(data, hours):
    for _ in range(hours):
        increase_saturation(data)
        draw_chart(data)
        sleep(1)


def decrease_with_sleep(data, hours):
    for _ in range(hours):
        decrease_saturation(data)
        draw_chart(data)
        sleep(1)


title_slot = st.empty()
figure_slot = st.empty()

for day in range(1, 6):
    with title_slot:
        st.markdown(f"### Day {day}")
    with figure_slot:
        increase_with_sleep(data, 1)
        decrease_with_sleep(data, 2)  # 9H00 - 11H00
        increase_with_sleep(data, 1)  # 11H00 - 12H00
        decrease_with_sleep(data, 3)  # 12H00 - 15H00
        increase_with_sleep(data, 1)  # 15H00 - 16H00
        decrease_with_sleep(data, 2)  # 16H00 - 18H00
        increase_with_sleep(data, 1)  # 18H00 - 19H00
        decrease_with_sleep(data, 13)  # 19H00 - 8H00

st.latex(r"""
\begin{aligned}
N(t) &= N_0 \times \left(\frac{1}{2}\right)^{\frac{t}{T_{1/2}}} \\
\\
N(t) & : \text{ quantité restante au temps } t \\
N_0 & : \text{ quantité initiale} \\
T_{1/2} & : \text{ demi-vie} \\
t & : \text{ temps écoulé}
\end{aligned}
""")
