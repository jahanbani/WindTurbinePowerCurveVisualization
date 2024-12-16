import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.graph_objects as go

# Load and preprocess the data
# file_path = "In_PowerCurves_Dut.csv"  # Update with the correct file path
file_path = "In_PowerCurves_Dut.csv"  # Replace with actual file path
data = pd.read_csv(file_path)

# Melt the data to long format
data_long = pd.melt(
    data, id_vars=["Speed bin (m/s)"], var_name="Wind Speed", value_name="Power"
)
data_long.rename(columns={"Speed bin (m/s)": "Turbine"}, inplace=True)
data_long["Wind Speed"] = data_long["Wind Speed"].astype(float)

# Sort turbines alphabetically
turbines = sorted(data_long["Turbine"].unique())

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# App layout with left-right structure
app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "row",
        "justifyContent": "space-between",
        "padding": "20px",
    },
    children=[
        # Left Section: Multi-select dropdown for turbines
        html.Div(
            style={"width": "30%", "padding": "10px"},
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
                        # "maxHeight": "400px",
                        # "overflowY": "auto",
                    },
                    maxHeight=400,
                ),
                html.Div(
                    id="warning-message",
                    style={"color": "red", "textAlign": "center", "marginTop": "10px"},
                ),
            ],
        ),
        # Right Section: Graph display
        html.Div(
            style={"width": "65%", "padding": "10px"},
            children=[
                html.H3(
                    "Power Curves", style={"textAlign": "center", "color": "#2C3E50"}
                ),
                dcc.Graph(id="power-curve-plot"),
            ],
        ),
    ],
)


# Callback for dynamic plotting with restrictions
@app.callback(
    [Output("power-curve-plot", "figure"), Output("warning-message", "children")],
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

    # Update layout for the plot
    fig.update_layout(
        title="Power Curves for Selected Turbines",
        xaxis_title="Wind Speed (m/s)",
        yaxis_title="Power (kW)",
        template="plotly_white",
        font=dict(family="Arial", size=12),
        hovermode="closest",
    )

    # Return the figure and no warning message
    return fig, ""


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
