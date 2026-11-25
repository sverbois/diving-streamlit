import streamlit as st
import streamlit.components.v1 as components

R = 0.08314  # L·bar/(mol·K)

st.title("Ideal Gas Law")
with st.expander("Description"):
    st.markdown(
        "The ideal gas law describes the relationship between pressure, volume, temperature, and the amount of a gas. "
        "It assumes gas molecules have no volume and no interactions. "
        "Adjust the sliders to see how each variable affects the others and observe the molecule animation."
    )

st.latex(r"PV = nRT \quad \text{with } R = 0.08314 \text{ L·bar·mol}^{-1}\text{·K}^{-1}")

col_controls, col_animation = st.columns([2, 3])

with col_controls:
    with st.container(border=True):
        V = st.slider("Volume V (L)", min_value=1, max_value=20, value=12, step=1, key="igv")
        n = st.slider("Amount of substance n (mol)", min_value=1, max_value=500, value=50, step=1, key="ign")
        T = st.slider("Temperature T (K)", min_value=233, max_value=373, value=293, step=1, key="igt")
        st.caption(f"= {T - 273:.0f} °C")
        st.divider()
        P = (n * R * T) / V
        st.metric("Pressure P", f"{P:.2f} bar")

with col_animation:
    html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{
    margin: 0;
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 400px;
  }}
  canvas {{
    display: block;
  }}
</style>
</head>
<body>
<canvas id="gasCanvas" width="520" height="380"></canvas>
<script>
  const V = {V};
  const n = {n};
  const T = {T};

  const canvas = document.getElementById("gasCanvas");
  const ctx = canvas.getContext("2d");
  const CW = canvas.width;
  const CH = canvas.height;

  // Container size scales with V
  const V_MIN = 1, V_MAX = 20;
  const FRAC_MIN = 0.25, FRAC_MAX = 0.90;
  const frac = FRAC_MIN + (V - V_MIN) / (V_MAX - V_MIN) * (FRAC_MAX - FRAC_MIN);
  const boxW = CW * frac;
  const boxH = CH * frac;
  const boxX = (CW - boxW) / 2;
  const boxY = (CH - boxH) / 2;

  // Ball count scales with n
  const N_MIN = 1, N_MAX = 500;
  const B_MIN = 3, B_MAX = 60;
  const ballCount = Math.round(B_MIN + (n - N_MIN) / (N_MAX - N_MIN) * (B_MAX - B_MIN));

  // Ball speed scales with T
  const T_MIN = 233, T_MAX = 373;
  const S_MIN = 0.5, S_MAX = 6.0;
  const baseSpeed = S_MIN + (T - T_MIN) / (T_MAX - T_MIN) * (S_MAX - S_MIN);

  const BALL_RADIUS = 5;
  const BALL_COLOR = "#e07b39";
  const BOX_COLOR = "#4a90d9";
  const BOX_LINE_WIDTH = 3;

  // Initialize balls inside the container
  const balls = [];
  for (let i = 0; i < ballCount; i++) {{
    const angle = Math.random() * 2 * Math.PI;
    const speed = baseSpeed * (0.8 + Math.random() * 0.4);
    balls.push({{
      x: boxX + BALL_RADIUS + Math.random() * (boxW - 2 * BALL_RADIUS),
      y: boxY + BALL_RADIUS + Math.random() * (boxH - 2 * BALL_RADIUS),
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
    }});
  }}

  function drawContainer() {{
    ctx.strokeStyle = BOX_COLOR;
    ctx.lineWidth = BOX_LINE_WIDTH;
    ctx.strokeRect(boxX, boxY, boxW, boxH);
  }}

  function moveBalls() {{
    for (const b of balls) {{
      b.x += b.vx;
      b.y += b.vy;
      // Bounce off walls
      if (b.x - BALL_RADIUS < boxX) {{
        b.x = boxX + BALL_RADIUS;
        b.vx = Math.abs(b.vx);
      }} else if (b.x + BALL_RADIUS > boxX + boxW) {{
        b.x = boxX + boxW - BALL_RADIUS;
        b.vx = -Math.abs(b.vx);
      }}
      if (b.y - BALL_RADIUS < boxY) {{
        b.y = boxY + BALL_RADIUS;
        b.vy = Math.abs(b.vy);
      }} else if (b.y + BALL_RADIUS > boxY + boxH) {{
        b.y = boxY + boxH - BALL_RADIUS;
        b.vy = -Math.abs(b.vy);
      }}
    }}
  }}

  function drawBalls() {{
    ctx.fillStyle = BALL_COLOR;
    for (const b of balls) {{
      ctx.beginPath();
      ctx.arc(b.x, b.y, BALL_RADIUS, 0, 2 * Math.PI);
      ctx.fill();
    }}
  }}

  function draw() {{
    ctx.clearRect(0, 0, CW, CH);
    drawContainer();
    moveBalls();
    drawBalls();
    requestAnimationFrame(draw);
  }}

  requestAnimationFrame(draw);
</script>
</body>
</html>
"""
    components.html(html, height=410)
