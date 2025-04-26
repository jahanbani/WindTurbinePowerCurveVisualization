#!/usr/bin/env python3
import os
import sys
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

# Print information for debugging
print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("Directory contents:", os.listdir('.'))

# Check if we can find the CSV file
data_file = "In_PowerCurves_Dut.csv"
print(f"Looking for data file: {data_file}")
if os.path.exists(data_file):
    print(f"Found data file: {data_file}")
else:
    print(f"Data file not found: {data_file}")
    print("Searching in parent directories...")
    for root, dirs, files in os.walk('/'):
        if data_file in files:
            data_file = os.path.join(root, data_file)
            print(f"Found data file at: {data_file}")
            break

# Load and preprocess the data
try:
    data = pd.read_csv(data_file)
    print(f"Successfully loaded data with {len(data)} rows")
    
    # Melt the data to long format
    data_long = pd.melt(
        data, id_vars=["Speed bin (m/s)"], var_name="Wind Speed", value_name="Power"
    )
    data_long.rename(columns={"Speed bin (m/s)": "Turbine"}, inplace=True)
    data_long["Wind Speed"] = data_long["Wind Speed"].astype(float)

    # Sort turbines alphabetically
    turbines = sorted(data_long["Turbine"].unique())
    print(f"Found {len(turbines)} turbines")

    # Initialize Dash app with meta tags for mobile responsiveness
    app = dash.Dash(
        __name__,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
        ]
    )
    
    # Ensure server variable exists
    server = app.server

    # App layout with responsive design
    app.layout = html.Div(
        style={
            "display": "flex",
            "flexDirection": "column",  # Default to column for mobile
            "padding": "10px",
            "maxWidth": "100%",
        },
        className="container",
        children=[
            # Header
            html.H2(
                "Wind Turbine Power Curve Visualization",
                style={"textAlign": "center", "color": "#2C3E50", "marginBottom": "20px"},
            ),
            
            # Selection Section
            html.Div(
                style={
                    "width": "100%", 
                    "padding": "10px",
                    "marginBottom": "20px"
                },
                children=[
                    html.H3(
                        "Select Wind Turbines",
                        style={"textAlign": "center", "color": "#2C3E50"},
                    ),
                    dcc.Dropdown(
                        id="turbine-dropdown",
                        options=[
                            {"label": turbine, "value": turbine} for turbine in turbines
                        ],
                        value=[turbines[0]],  # Default selection
                        multi=True,  # Allow multi-selection
                        style={
                            "fontSize": "14px",
                        },
                        maxHeight=400,
                    ),
                    html.Div(
                        id="warning-message",
                        style={"color": "red", "textAlign": "center", "marginTop": "10px"},
                    ),
                ],
            ),
            
            # Graph display
            html.Div(
                style={"width": "100%", "padding": "10px"},
                children=[
                    html.H3(
                        "Power Curves", style={"textAlign": "center", "color": "#2C3E50"}
                    ),
                    dcc.Graph(
                        id="power-curve-plot",
                        config={
                            'responsive': True,
                            'displayModeBar': True,
                            'displaylogo': False,
                            'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                        },
                        style={'height': '60vh'}  # Responsive height
                    ),
                ],
            ),
        ],
    )

    # Callback for dynamic plotting with restrictions
    @app.callback(
        [Output("power-curve-plot", "figure"),
         Output("warning-message", "children")],
        [Input("turbine-dropdown", "value")],
    )
    def update_plot(selected_turbines):
        # Restrict to a maximum of 3 turbines
        if len(selected_turbines) > 3:
            return go.Figure(), "Please select up to 3 turbines only."

        # Initialize a figure
        fig = go.Figure()

        # Add a line for each selected turbine
        for turbine in selected_turbines:
            filtered_data = data_long[data_long["Turbine"] == turbine]
            fig.add_trace(
                go.Scatter(
                    x=filtered_data["Wind Speed"],
                    y=filtered_data["Power"],
                    mode="lines+markers",
                    name=turbine,  # Show turbine name in legend
                    # Turbine name as hover text
                    text=[turbine] * len(filtered_data),
                    # Show text (turbine name) and coordinates
                    hoverinfo="text+x+y",
                    line=dict(width=2),
                )
            )

        # Update layout for the plot with mobile-friendly settings
        fig.update_layout(
            title="Power Curves for Selected Turbines",
            xaxis_title="Wind Speed (m/s)",
            yaxis_title="Power (kW)",
            template="plotly_white",
            font=dict(family="Arial", size=12),
            hovermode="closest",
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=40, r=20, t=60, b=40),  # Tighter margins
            autosize=True,
        )

        # Return the figure and no warning message
        return fig, ""

    # Run the app
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 4000))
        print(f"Starting server on port {port}")
        app.run(host="0.0.0.0", port=port, debug=False)
        
except Exception as e:
    print(f"ERROR: {str(e)}")
    print("Stack trace:")
    import traceback
    traceback.print_exc() 