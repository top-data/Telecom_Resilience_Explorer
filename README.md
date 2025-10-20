# Telecom Resilience Explorer

Telecom Resilience Explorer is an interactive Streamlit dashboard for visualizing telecommunications networks across geographic maps and for running failure simulations to assess cascading impacts and recovery planning. It's intended as a prototype and starting point for vulnerability analysis and stakeholder-facing dashboards.

Key features
- Geospatial visualization of sites and links (Plotly + Mapbox)
- Layered views (Physical, Logical, Management)
- Failure simulation engine with cascading propagation and timeline
- Interactive node metadata and dependency exploration (planned enhancements)

Status
- Prototype: core visualization, data model, and a simple simulation engine are implemented.
- Designed for extension: add richer dependency models, resilience scoring, animations, and playback.

Quick start (Windows PowerShell)

1. Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the Streamlit app:

```powershell
streamlit run app.py
```

Configuration
- Mapbox: The app uses Plotly Mapbox for map rendering. For production, provide a valid Mapbox access token. You can set it via an environment variable and the visualization helper will pick it up, or modify `utils/visualization.py` to inject the token.

Data format
The app expects a JSON topology in `data/network_topology.json` with entries like:

```json
{
	"site": "Sydney Data Centre",
	"lat": -33.8688,
	"lon": 151.2093,
	"sovereign": ["BGP", "DNS", "NTP"],
	"supporting": ["AAA", "LicenseMgmt"],
	"dependencies": ["Melbourne Hub", "Brisbane Core"]
}
```

Project layout

```
telecom_resilience_explorer/
├── app.py                     # Main Streamlit entry point
├── data/
│   └── network_topology.json  # Sample network definition
├── utils/
│   ├── graph_utils.py         # NetworkX graph helpers
│   ├── simulation.py          # Failure propagation logic
│   └── visualization.py       # Plotly / Mapbox map renderers
├── assets/
│   ├── icons/                 # Optional function icons
│   └── styles.css             # Custom styles
├── requirements.txt
└── README.md
```

How it works (high-level)
- The app loads the JSON topology and constructs a NetworkX DiGraph using `utils/graph_utils.py`.
- `utils/simulation.py` provides a simple stochastic cascading model: given seed failures, dependent nodes may fail over time and the simulator returns a timeline of events.
- `utils/visualization.py` draws nodes and dependency edges on a Mapbox map using Plotly and marks failed nodes.

Next steps / TODOs
- Node click interaction: show a sidebar with node metadata, dependencies and a small subgraph.
- Playback/timeline panel with event logs and severity coloring.
- Add unit tests for graph logic and simulation.
- Replace placeholder Mapbox token and support layered style definitions (YAML/TOML).

Contributing
- Contributions are welcome. Open an issue to discuss major changes.
- For code changes, please fork, create a feature branch, and open a pull request.

License
- MIT License (placeholder) — add your preferred license.

