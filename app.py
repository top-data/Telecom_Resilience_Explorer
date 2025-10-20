import streamlit as st
from utils.visualization import MapVisualizer
from utils.graph_utils import build_graph_from_topology
from utils.simulation import simulate_failure
import json
import pandas as pd

st.set_page_config(layout="wide", page_title="Network Resilience Explorer")

@st.cache_data
def load_topology(path="data/network_topology.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

topology = load_topology()
G = build_graph_from_topology(topology)

st.sidebar.title("Simulation Controls")
layer = st.sidebar.selectbox("Network Layer", ["Physical", "Logical", "Management"]) 
failure_type = st.sidebar.selectbox("Failure Type", ["DNS", "BGP", "NTP", "AAA", "License"])
impact = st.sidebar.radio("Impact Scope", ["Local", "Regional", "National"])
duration = st.sidebar.slider("Duration (hours)", 1, 24, 6)

st.header("Telecom Resilience Explorer (NRE) — Australia")

col1, col2 = st.columns((3,1))

with col1:
    mv = MapVisualizer(topology)
    fig = mv.plot_map(layer=layer, failed_nodes=[]) 
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Selected Node Details")
    st.info("Click a node on the map to view details (interactive).")
    st.subheader("Active Alerts")
    st.write("No active simulated outages")

st.sidebar.markdown("---")
if st.sidebar.button("Run Simulation"):
    failed, timeline = simulate_failure(G, topology, failure_type, impact, duration)
    st.sidebar.success(f"Simulation complete — {len(failed)} failed nodes")
    with col1:
        fig2 = mv.plot_map(layer=layer, failed_nodes=failed, timeline=timeline)
        st.plotly_chart(fig2, use_container_width=True)
