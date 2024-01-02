import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Create a sample DataFrame (replace this with your actual dataset)
data = {
    "age": [63, 37, 41, 56, 57, 57, 56, 44, 52, 57],
    "sex": [1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    "cp": [3, 2, 1, 1, 0, 0, 1, 1, 2, 2],
    "trtbps": [145, 130, 130, 120, 120, 140, 140, 120, 172, 150],
    "chol": [233, 250, 204, 236, 354, 192, 294, 263, 199, 168],
    "fbs": [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    "restecg": [0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
    "thalachh": [150, 187, 172, 178, 163, 148, 153, 173, 162, 174],
    "exng": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    "oldpeak": [2.3, 3.5, 1.4, 0.8, 0.6, 0, 0.4, 1.6, 0.5, 1.6],
    "slp": [0, 0, 2, 2, 2, 1, 1, 2, 2, 2],
    "caa": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "thall": [1, 2, 2, 2, 2, 1, 2, 3, 3, 2],
    "output": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
}

df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div(
    [
        html.H1("Heart Disease Dashboard"),
        # KPIs
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Average Age"),
                        html.P(id="kpi-age", style={"font-size": "24px"}),
                    ],
                    className="kpi-card",
                ),
                html.Div(
                    [
                        html.H3("Percentage of Females"),
                        html.P(id="kpi-female-percentage", style={"font-size": "24px"}),
                    ],
                    className="kpi-card",
                ),
                html.Div(
                    [
                        html.H3("Average Resting Blood Pressure"),
                        html.P(id="kpi-trtbps", style={"font-size": "24px"}),
                    ],
                    className="kpi-card",
                ),
            ],
            className="kpi-container",
        ),
        # Charts
        html.Div(
            [
                # Histogram of Age
                dcc.Graph(
                    id="histogram-age",
                    figure=px.histogram(
                        df,
                        x="age",
                        color="output",
                        marginal="rug",
                        title="Age Distribution",
                    ),
                ),
                # Scatter Plot of Resting Blood Pressure vs. Cholesterol
                dcc.Graph(
                    id="scatter-trtbps-chol",
                    figure=px.scatter(
                        df,
                        x="trtbps",
                        y="chol",
                        color="output",
                        title="Resting BP vs. Cholesterol",
                    ),
                ),
                # Bar Chart of Chest Pain Types
                dcc.Graph(
                    id="bar-cp",
                    figure=px.bar(
                        df,
                        x="cp",
                        color="output",
                        barmode="group",
                        title="Chest Pain Types",
                    ),
                ),
                # Pie Chart of Gender Distribution
                dcc.Graph(
                    id="pie-gender",
                    figure=px.pie(df, names="sex", title="Gender Distribution"),
                ),
            ],
            className="chart-container",
        ),
    ]
)


# Callbacks to update KPI values dynamically
@app.callback(
    [
        Output("kpi-age", "children"),
        Output("kpi-female-percentage", "children"),
        Output("kpi-trtbps", "children"),
    ],
    [Input("histogram-age", "selectedData")],
)
def update_kpis(selected_data):
    avg_age = df["age"].mean()
    female_percentage = (df["sex"] == 0).mean() * 100
    avg_trtbps = df["trtbps"].mean()

    return (
        f"{avg_age:.2f} years",
        f"{female_percentage:.2f}%",
        f"{avg_trtbps:.2f} mm Hg",
    )


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
