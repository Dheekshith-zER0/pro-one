# app.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="MaxwellXR — Real-Time 3D Field Visualizer ∞ Prototype")

st.title("MaxwellXR — Real-Time 3D Electromagnetic Field Visualizer ∞ Prototype")
st.markdown("Interactive demo: 3D vector field (cones) for point charge or dipole. Use sliders to change parameters. This is a rapid prototype and will evolve into AR/VR.")

# Sidebar controls
st.sidebar.header("Controls")
mode = st.sidebar.radio("Field type", ("Single point charge", "Dipole (oscillating)"))
q = st.sidebar.slider("Charge magnitude (q)", -5.0, 5.0, 1.0, step=0.1)
scale = st.sidebar.slider("Arrow scale (visual)", 0.1, 5.0, 1.0, step=0.1)
grid_n = st.sidebar.selectbox("Grid resolution (coarse → fast)", [8, 10, 12, 15], index=1)
show_charge = st.sidebar.checkbox("Show charge(s) position", True)
t = st.sidebar.slider("Time (for dipole oscillation)", 0.0, 2*np.pi, 0.0, step=0.1)

# Create a 3D grid
L = 1.0
n = int(grid_n)
xs = np.linspace(-L, L, n)
ys = np.linspace(-L, L, n)
zs = np.linspace(-L, L, n)
X, Y, Z = np.meshgrid(xs, ys, zs, indexing="xy")

# Flatten for vector math
x = X.ravel()
y = Y.ravel()
z = Z.ravel()

# Field calculation
def E_point_charge(qval, rx, ry, rz, pos):
    dx = rx - pos[0]
    dy = ry - pos[1]
    dz = rz - pos[2]
    r3 = (dx**2 + dy**2 + dz**2) ** 1.5
    eps = 1e-6
    r3 = np.where(r3 < eps, eps, r3)
    k = 1.0  # scaled for visualization
    return k*qval*dx/r3, k*qval*dy/r3, k*qval*dz/r3

# Select mode
if mode == "Single point charge":
    qpos = (0.0, 0.0, 0.0)
    Ex, Ey, Ez = E_point_charge(q, x, y, z, qpos)

else:
    sep = 0.4
    q1 = q * np.sin(t)
    q2 = -q1
    pos1 = (-sep/2, 0.0, 0.0)
    pos2 = ( sep/2, 0.0, 0.0)

    E1 = E_point_charge(q1, x, y, z, pos1)
    E2 = E_point_charge(q2, x, y, z, pos2)

    Ex = E1[0] + E2[0]
    Ey = E1[1] + E2[1]
    Ez = E1[2] + E2[2]

# Scaling vectors
mag = np.sqrt(Ex**2 + Ey**2 + Ez**2)
mag_max = max(np.percentile(mag, 95), 1e-6)
u = Ex / mag_max * scale
v = Ey / mag_max * scale
w = Ez / mag_max * scale

mask = (np.sqrt(x**2 + y**2 + z**2) > 0.07)
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
    opacity=0.8
))

if show_charge:
    if mode == "Single point charge":
        fig.add_trace(
            go.Scatter3d(
                x=[0], y=[0], z=[0],
                mode="markers",
                marker=dict(size=6, color='red' if q>0 else 'blue')
            )
        )
    else:
        fig.add_trace(
            go.Scatter3d(
                x=[pos1[0], pos2[0]],
                y=[0, 0],
                z=[0, 0],
                mode="markers",
                marker=dict(size=6, color=['red', 'blue'])
            )
        )

fig.update_layout(
    scene=dict(
        xaxis=dict(showticklabels=False, title=''),
        yaxis=dict(showticklabels=False, title=''),
        zaxis=dict(showticklabels=False, title=''),
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, t=30, b=0),
    height=720
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Info:
- This is a simplified electric field visualizer.
- Vectors are scaled visually.
- Dipole mode uses sinusoidal oscillation (prototype behaviour).
""")

st.markdown("---")
st.write("Team SKYNET | MaxwellXR ∞ Prototype")

