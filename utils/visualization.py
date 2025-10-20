import plotly.graph_objects as go
import pandas as pd

class MapVisualizer:
    def __init__(self, topology, mapbox_token=None):
        self.topology = topology
        self.mapbox_token = mapbox_token or "pk.eyJ1IjoiZGVtbzEiLCJhIjoiY2todDg5eG1lMGZ5bTJvcGQ5bWZ6b2E1biJ9.FAKE_TOKEN"

    def _nodes_df(self):
        return pd.DataFrame([{
            "site": n.get("site"),
            "lat": n.get("lat"),
            "lon": n.get("lon"),
            "sovereign": ",".join(n.get("sovereign", [])),
            "supporting": ",".join(n.get("supporting", []))
        } for n in self.topology])

    def plot_map(self, layer="Physical", failed_nodes=None, timeline=None):
        df = self._nodes_df()
        failed_nodes = failed_nodes or []

        fig = go.Figure()

        # nodes
        fig.add_trace(go.Scattermapbox(
            lat=df['lat'], lon=df['lon'], mode='markers+text',
            marker=dict(size=12, color=["red" if s in failed_nodes else "blue" for s in df['site']]),
            text=df['site'], textposition='top right', hoverinfo='text'
        ))

        # edges from dependencies
        for node in self.topology:
            src = node.get('site')
            for dep in node.get('dependencies', []):
                dep_node = next((n for n in self.topology if n.get('site') == dep), None)
                if dep_node:
                    fig.add_trace(go.Scattermapbox(
                        lat=[node.get('lat'), dep_node.get('lat')],
                        lon=[node.get('lon'), dep_node.get('lon')],
                        mode='lines', line=dict(width=2, color='green' if layer=='Physical' else 'orange'),
                        hoverinfo='none'
                    ))

        fig.update_layout(mapbox_style='carto-positron', mapbox_accesstoken=self.mapbox_token,
                          mapbox=dict(center=dict(lat=-25, lon=133), zoom=3.2))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        return fig
