import plotly.graph_objects as go
import streamlit as st

st.title("Gradient Factors")
fig = go.Figure()

x1 = [0, 10, 20, 30, 40, 50]
y1 = [0, 10, 20, 30, 40, 50]
fig.add_trace(go.Scatter(x=x1, y=y1, mode="lines", name="TODO1"))

x2 = [0, 20, 40, 40, 40]
y2 = [0, 0, 0, 6, 10, 16]
labels = [f"{i}min" for i in range(len(y2))]
fig.add_trace(
    go.Scatter(
        x=x2,
        y=y2,
        mode="lines+markers+text",
        name="Plongée",
        text=labels,
        textposition="top center",
        hoverinfo="skip",
    )
)
fig.update_layout(
    xaxis_title="Pression / Profondeur(m)",
    yaxis_title="Tension",
    xaxis=dict(showgrid=False, zeroline=True, zerolinewidth=1, zerolinecolor="black"),
    yaxis=dict(showgrid=False, zeroline=True, zerolinewidth=1, zerolinecolor="black", showticklabels=False),
)
st.plotly_chart(fig, use_container_width=True)
