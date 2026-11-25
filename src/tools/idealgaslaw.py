import json

import streamlit as st

from config import CYLINDER_VOLUMES
from config import DEFAULT_CYLINDER_VOLUME_INDEX
from utils import celsius
from utils import ideal_gas_pressure
from utils import kelvin
from utils import moles_in
from utils import surface_volume_of

MAX_MOLES = 300  # about a 24 L cylinder at 300 bar
DEFAULT_MOLES = 123  # a 15 L cylinder at 200 bar
MIN_CELSIUS = -5
MAX_CELSIUS = 50
DEFAULT_CELSIUS = 20
MAX_PARTICLES = 120
# Streamlit's default text colors, so the cylinder stays visible in the light and dark themes.
BORDER = {"light": "#31333F", "dark": "#FAFAFA"}

ANIMATION = """
<!DOCTYPE html>
<html>
<body style="margin: 0">
<canvas id="gas" height="200" style="display: block; width: 100%"></canvas>
<script>
  const p = __PARAMS__;
  const canvas = document.getElementById("gas");
  canvas.width = canvas.clientWidth;
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  const RADIUS = 4;

  // The body area follows the cylinder volume, so particle density on screen follows pressure.
  const scale = Math.sqrt(p.volume / p.maxVolume);
  let bodyH = 0.95 * H * scale;
  // Overall length (body, neck and valve) in units of body height, shrunk to fit narrow screens.
  const LENGTH = 2.8 + 0.15 + 0.13;
  bodyH = Math.min(bodyH, (0.95 * W) / LENGTH);
  const bodyW = 2.8 * bodyH, r = bodyH / 2;
  const bodyX = (W - LENGTH * bodyH) / 2, bodyY = (H - bodyH) / 2, cy = bodyY + r;
  const leftCap = bodyX + r, rightCap = bodyX + bodyW - r;
  const neck = { x: bodyX + bodyW, w: 0.15 * bodyH, h: 0.25 * bodyH };
  const valve = { x: neck.x + neck.w, w: 0.13 * bodyH, h: 0.3 * bodyH };

  // Real speed only varies by 10 % over the slider range, so it is stretched to show it.
  const heat = (p.temperature - p.minTemperature) / (p.maxTemperature - p.minTemperature);
  const speed = 0.5 + heat * 5.5;

  const particles = Array.from({ length: p.count }, () => {
    const angle = 2 * Math.PI * Math.random();
    return {
      x: leftCap + Math.random() * (rightCap - leftCap),
      y: bodyY + RADIUS + Math.random() * (bodyH - 2 * RADIUS),
      vx: speed * Math.cos(angle),
      vy: speed * Math.sin(angle),
    };
  });

  // The body is a capsule: flat walls along its length, half-circle domes at both ends.
  function collide(q) {
    if (q.x > leftCap && q.x < rightCap) {
      if (q.y < bodyY + RADIUS) [q.y, q.vy] = [bodyY + RADIUS, Math.abs(q.vy)];
      if (q.y > bodyY + bodyH - RADIUS) [q.y, q.vy] = [bodyY + bodyH - RADIUS, -Math.abs(q.vy)];
      return;
    }
    const cx = q.x <= leftCap ? leftCap : rightCap;
    const dx = q.x - cx, dy = q.y - cy, d = Math.hypot(dx, dy), limit = r - RADIUS;
    if (d <= limit) return;
    const nx = dx / d, ny = dy / d, dot = q.vx * nx + q.vy * ny;
    if (dot > 0) [q.vx, q.vy] = [q.vx - 2 * dot * nx, q.vy - 2 * dot * ny];
    [q.x, q.y] = [cx + nx * limit, cy + ny * limit];
  }

  function drawCylinder() {
    ctx.strokeStyle = p.border;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(bodyX, bodyY, bodyW, bodyH, r);
    ctx.rect(neck.x, cy - neck.h / 2, neck.w, neck.h);
    ctx.roundRect(valve.x, cy - valve.h / 2, valve.w, valve.h, 3);
    ctx.stroke();
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    drawCylinder();
    ctx.fillStyle = "#808495";
    for (const q of particles) {
      q.x += q.vx;
      q.y += q.vy;
      collide(q);
      ctx.beginPath();
      ctx.arc(q.x, q.y, RADIUS, 0, 2 * Math.PI);
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);
</script>
</body>
</html>
"""

st.title("Ideal Gas Law")
with st.expander("Description"):
    st.markdown(
        "The ideal gas law links the pressure, volume, temperature and amount of a gas. "
        "In a diving cylinder the volume is fixed: adding gas or warming it up raises the pressure. "
        "In the animation, the particles speed up with the temperature; "
        "the speed change is exaggerated to make it visible."
    )

st.latex(r"""
\begin{array}{c c l}
\Large P V = n R T & \text{where} &
\begin{array}{l}
P := \text{ Pressure (bar)} \\
V := \text{ Volume (L)} \\
n := \text{ Amount of gas (mol)} \\
R := \text{ 0.08314 L·bar/(mol·K)} \\
T := \text{ Temperature (K)}
\end{array}
\end{array}
""")

st.session_state.setdefault("idealgaslaw_moles", DEFAULT_MOLES)
st.session_state.setdefault("idealgaslaw_surface_volume", round(surface_volume_of(DEFAULT_MOLES)))
st.session_state.setdefault("idealgaslaw_kelvin", round(kelvin(DEFAULT_CELSIUS)))
st.session_state.setdefault("idealgaslaw_celsius", DEFAULT_CELSIUS)


def sync_surface_volume():
    st.session_state.idealgaslaw_surface_volume = round(surface_volume_of(st.session_state.idealgaslaw_moles))


def sync_moles():
    st.session_state.idealgaslaw_moles = round(moles_in(st.session_state.idealgaslaw_surface_volume))


def sync_celsius():
    st.session_state.idealgaslaw_celsius = round(celsius(st.session_state.idealgaslaw_kelvin))


def sync_kelvin():
    st.session_state.idealgaslaw_kelvin = round(kelvin(st.session_state.idealgaslaw_celsius))


with st.container(border=True):
    col_volume, _ = st.columns(2)
    volume = col_volume.select_slider(
        "Cylinder volume V (in L)",
        options=CYLINDER_VOLUMES,
        value=CYLINDER_VOLUMES[DEFAULT_CYLINDER_VOLUME_INDEX],
        key="idealgaslaw_volume",
    )
    col_moles, col_litres = st.columns(2)
    moles = col_moles.slider(
        "Amount of gas n (in mol)",
        min_value=0,
        max_value=MAX_MOLES,
        step=1,
        key="idealgaslaw_moles",
        on_change=sync_surface_volume,
    )
    col_litres.slider(
        "Gas at 1 bar and 20 °C (in L)",
        min_value=0,
        max_value=round(surface_volume_of(MAX_MOLES)),
        step=1,
        key="idealgaslaw_surface_volume",
        on_change=sync_moles,
    )
    col_kelvin, col_celsius = st.columns(2)
    temperature = col_kelvin.slider(
        "Temperature T (in K)",
        min_value=round(kelvin(MIN_CELSIUS)),
        max_value=round(kelvin(MAX_CELSIUS)),
        step=1,
        key="idealgaslaw_kelvin",
        on_change=sync_celsius,
    )
    col_celsius.slider(
        "Temperature (in °C)",
        min_value=MIN_CELSIUS,
        max_value=MAX_CELSIUS,
        step=1,
        key="idealgaslaw_celsius",
        on_change=sync_kelvin,
    )
    pressure = ideal_gas_pressure(volume, moles, temperature)
    st.markdown(f"## P = {pressure:.0f} bar", text_alignment="center")

params = {
    "volume": volume,
    "maxVolume": max(CYLINDER_VOLUMES),
    "count": round(moles / MAX_MOLES * MAX_PARTICLES),
    "temperature": temperature,
    "minTemperature": kelvin(MIN_CELSIUS),
    "maxTemperature": kelvin(MAX_CELSIUS),
    "border": BORDER["dark" if st.context.theme.type == "dark" else "light"],
}
st.iframe(
    ANIMATION.replace("__PARAMS__", json.dumps(params)),
    height=210,
    alt="Gas particles moving in the cylinder, faster as the temperature rises",
)
