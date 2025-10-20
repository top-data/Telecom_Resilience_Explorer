# Telecom Resilience Explorer

Interactive Streamlit dashboard to visualize telecom networks and simulate failures.

How to run

1. Create a virtual environment and install requirements:

```
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Run Streamlit:

```
streamlit run app.py
```

Files
- `app.py` — main Streamlit app
- `data/network_topology.json` — sample topology
- `utils/` — helper modules for graph, simulation, and visualization
