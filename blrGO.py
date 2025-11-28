import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="MaxwellXR — Real-Time 3D Field Visualizer ∞ Prototype")

st.title("MaxwellXR — Real-Time 3D Electromagnetic Field Visualizer ∞ Prototype")
st.markdown(
    "Interactive 3D vector field generated using Coulomb's law. "
    "This is a rapid prototype for demonstrating the concept."
)

# Sidebar controls
st.sidebar.header("Controls")
mode = st.sidebar.radio("Field Type", ("Single Point Charge", "Dipole (Oscillating)"))
q = st.sidebar.slider("Charge Magnitude (q)", -5.0, 5.0, 1.0, step=0.1)
scale = st.sidebar.slider("Arrow Scale", 0.1, 5.0, 1.0, step=0.1)
grid_n = st.sidebar.selectbox("Grid Resolution", [8, 10, 12, 15], index=1)
show_charge = st.sidebar.checkbox("Show Charges", True)
t = st.sidebar.slider("Time (Dipole Oscillation)", 0.0, 6.28, 0.0, step=0.1)

# Create grid
L = 1.0
n = int(grid_n)
xs = np.linspace(-L, L, n)
ys = np.linspace(-L, L, n)
zs = np.linspace(-L, L, n)
X, Y, Z = np.meshgrid(xs, ys, zs, indexing="xy")

# Flatten
x, y, z = X.ravel(), Y.ravel(), Z.ravel()

def electric_field(qval, rx, ry, rz, pos):
    dx = rx - pos[0]
    dy = ry - pos[1]
    dz = rz - pos[2]

    r3 = (dx*dx + dy*dy + dz*dz)**1.5
    r3 = np.where(r3 < 1e-6, 1e-6, r3)

    k = 1.0
    return k*qval*dx/r3, k*qval*dy/r3, k*qval*dz/r3

# Field modes
if mode == "Single Point Charge":
    pos = (0.0, 0.0, 0.0)
    Ex, Ey, Ez = electric_field(q, x, y, z, pos)

else:
    sep = 0.4
    q1 = q * np.sin(t)
    q2 = -q1
    pos1 = (-sep/2, 0.0, 0.0)
    pos2 = ( sep/2, 0.0, 0.0)

    E1 = electric_field(q1, x, y, z, pos1)
    E2 = electric_field(q2, x, y, z, pos2)

    Ex = E1[0] + E2[0]
    Ey = E1[1] + E2[1]
    Ez = E1[2] + E2[2]

# Scale
mag = np.sqrt(Ex*Ex + Ey*Ey + Ez*Ez)
mag_max = max(np.percentile(mag, 95), 1e-6)

u = Ex / mag_max * scale
v = Ey / mag_max * scale
w = Ez / mag_max * scale

mask = (np.sqrt(x*x + y*y + z*z) > 0.07)
x_v, y_v, z_v = x[mask], y[mask], z[mask]
u_v, v_v, w_v = u[mask], v[mask], w[mask]

# Plot
fig = go.Figure()

fig.add_trace(go.Cone(
    x=x_v, y=y_v, z=z_v,
    u=u_v, v=v_v, w=w_v,
    sizemode="absolute",
    sizeref=0.4,
    showscale=False,
    anchor="tail",
    hoverinfo="skip",
    opacity=0.85
))

if show_charge:
    if mode == "Single Point Charge":
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode="markers",
            marker=dict(size=6, color="red" if q > 0 else "blue")
        ))
    else:
        fig.add_trace(go.Scatter3d(
            x=[pos1[0], pos2[0]],
            y=[0, 0],
            z=[0, 0],
            mode="markers",
            marker=dict(size=6, color=["red", "blue"])
        ))

fig.update_layout(
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        aspectmode="cube"
    ),
    height=720,
    margin=dict(l=0, r=0, t=30, b=0)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.write("Team SKYNET | MaxwellXR ∞ Prototype")
