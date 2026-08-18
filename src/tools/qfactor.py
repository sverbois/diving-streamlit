import pandas as pd
import streamlit as st

EXAMPLE_TIME = 25  # min, used to derive an example depth for each category below

CATEGORIES = [
    ("Recreational", 100),
    ("Recreational", 150),
    ("Sport", 200),
    ("Sport", 250),
    ("Sport", 300),
    ("Technical", 350),
    ("Technical", 400),
    ("Technical", 450),
    ("Expedition", 500),
    ("Expedition", 550),
    ("Expedition", 600),
]


def compute_q(depth, time):
    return depth * (time**0.5)


def category_for_q(q):
    if q < 200:
        return "Recreational"
    if q < 350:
        return "Sport"
    if q < 500:
        return "Technical"
    return "Expedition"


ROW_COLORS = {
    "Recreational": "green",
    "Sport": "blue",
    "Technical": "orange",
    "Expedition": "red",
}


def highlight_row(row):
    color = ROW_COLORS[row["Dive type"]]
    return [f"color: {color}"] * len(row)


def dci_risq_for_q(q):
    if q <= 100:
        return "1/1,000,000"
    if q <= 200:
        return "1/100,000"
    if q <= 300:
        return "1/10,000"
    if q <= 400:
        return "1/1,000"
    if q <= 450:
        return "2/100"
    if q <= 500:
        return "4/100"
    if q <= 550:
        return "6/100"
    if q <= 600:
        return "10/100"
    return "??/100"


st.title("Dive engagement / Q Factor")
with st.expander("Description"):
    st.markdown(
        "In 1952, Dr. Henry V. Hempleman introduced the Q Factor as a way to quantify the overall decompression "
        "engagement of a dive, combining depth and time into a single value. "
        "The higher the Q Factor, the greater the theoretical risk of decompression sickness."
    )

st.latex(r"""
\begin{array}{c c l}
\Large Q = D \times \sqrt{T} & \text{where} &
\begin{array}{l}
Q := \text{ Q Factor} \\
D := \text{ Depth (m)} \\
T := \text{ Time (min)}
\end{array}
\end{array}
""")

with st.container(border=True):
    l1c1, l1c2 = st.columns(2)
    qfactor_depth = l1c1.slider(
        label="Depth D (in m)",
        min_value=0,
        max_value=120,
        value=40,
        step=1,
        key="qfactor_depth",
    )
    qfactor_time = l1c2.slider(
        label="Time T (in min)",
        min_value=0,
        max_value=90,
        value=20,
        step=1,
        key="qfactor_time",
    )
    qfactor_q = compute_q(qfactor_depth, qfactor_time)
    st.markdown(
        f"<div class='center'><h3 class='center' style='color: {ROW_COLORS[category_for_q(qfactor_q)]}'>{category_for_q(qfactor_q)} Dive</h3>"
        f"<h2>Q = {qfactor_q:.1f}</h2></div>",
        unsafe_allow_html=True,
    )


st.header("Examples")
table = pd.DataFrame(
    [
        {
            "Time (min)": EXAMPLE_TIME,
            "Depth (m)": round(q / (EXAMPLE_TIME**0.5)),
            "Engagement (Q)": q,
            "Dive type": kind,
            "Risk of DCS": dci_risq_for_q(q),
        }
        for kind, q in CATEGORIES
    ]
)
st.dataframe(
    table.style.apply(highlight_row, axis=1),
    hide_index=True,
    width="content",
    height=(len(table) + 1) * 35 + 3,
)

st.header("DCS Risk")
st.info(
    "When Engagment (Q) is multiplied by 1.3, the DCS risk is multiplied by 10. "
    "This means that a dive with Q=200 has a DCS risk of 1/100,000, while a dive with Q=260 (200*1.3) has a DCS risk of 1/10,000."
)
st.markdown(
    "This overall statistical risk also varies depending on the diver and their behavior. "
    "Six criteria can be taken into account:\n"
    "1. Age and weight\n"
    "2. Medical history (injuries, DCS, PFO, lifestyle, diet, tobacco, alcohol, medication...)\n"
    "3. Not practicing a sport regularly\n"
    "4. Fatigue and stress before the dive (jet lag, dehydration)\n"
    "5. Exertion during and after the dive\n"
    "6. Decompression errors (ascending too fast, yo-yo diving, repetitive dives, skipped stops...)\n"
)
st.error("Each of these 6 factors multiplies the risk of DCS by a factor of 10!")
st.markdown(
    "**Example:** A diver combining 3 risk factors (e.g. age, no regular sport practice and fatigue before the dive) "
    "sees their DCS risk jump from 1/100,000 to 1/1,000 for the same dive profile."
)
