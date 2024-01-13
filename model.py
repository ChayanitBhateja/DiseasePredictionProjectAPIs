from fastapi import FastAPI
import pickle
import pandas as pd
import uvicorn
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import mpld3
import json
from fastapi.middleware.cors import CORSMiddleware
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI()

# xTest would be [[13 numeric values here...]]

# Allow all origins to access the API (replace "*" with your frontend URL in production)
origins = ["*"]

data = pd.read_csv("./dataset/heart.csv")

# Add CORS middleware to allow cross-origin requestsqualitative
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_prediction")
def get_prediction(
    age: int,
    sex: int,
    cp: int,
    trtbps: int,
    chol: int,
    fbs: int,
    restecg: int,
    thalachh: int,
    exng: int,
    oldpeak: float,
    slp: int,
    caa: int,
    thall: int,
):
    data = pd.DataFrame(
        [
            [
                age,
                sex,
                cp,
                trtbps,
                chol,
                fbs,
                restecg,
                thalachh,
                exng,
                oldpeak,
                slp,
                caa,
                thall,
            ]
        ]
    )
    model = pickle.load(open("model.pkl", "rb"))
    prediction: int
    prediction = int(model.predict(data)[0])
    # print(prediction)
    return {"prediction": prediction}

@app.get("/interactive_plot")
def get_interactive_plot():
    # Create a sample DataFrame (replace this with your actual dataset)
    df = pd.read_csv("./dataset/heart.csv")
    fig1Data = df["age"].value_counts().reset_index(name="count")
    fig1Data.columns = ["Age", "Count"]

    fig3Data = df["cp"].value_counts().reset_index(name="count")
    fig3Data.columns = ["CP", "Count"]

    fig4Data = df["sex"].value_counts().reset_index(name="count")
    fig4Data.columns = ["Sex", "Count"]
    # Plot 1: Histogram with Gradient using Marginal Plot
    fig1 = px.bar(
        fig1Data,
        x="Age",
        y="Count",
        title="Age Distribution",
        labels={"age": "Age", "count": "Frequency"},
        template="plotly_white",
        color="Age",
        color_continuous_scale=px.colors.sequential.Blues,
    )

    # Plot 2: Scatter Plot of Resting Blood Pressure vs. Cholesterol
    fig2 = px.scatter(
        df,
        x="trtbps",
        y="chol",
        color="output",
        # color_discrete_map={0: "#3D85C6", 1: "#E53935"},
        title="Resting BP vs. Cholesterol",
        labels={"trtbps": "Resting Blood Pressure", "chol": "Cholesterol"},
        template="plotly_white",
        marginal_y="box",
        marginal_x="box",
        color_discrete_sequence=px.colors.qualitative.D3_r,
    )
    fig2.update_layout(hovermode="x")    

    fig3 = px.scatter(
        fig3Data,
        x="CP",
        y="Count",
        color_discrete_map={
            "0": "#FFC107",
            "1": "#4CAF50",
            "2": "#E57373",
            "3": "#5E35B1",
        },
        size="Count",
    )

    # Plot 4: Bar Chart of Gender Distribution (Retained)
    fig4 = px.bar(
        fig4Data,
        x="Sex",
        y="Count",
        title="Gender Distribution",
        labels={"sex": "Sex", "count": "Frequency"},
        template="plotly_white",
        color="Sex",
        # color_discrete_map={
        #     "0": "#FFC107",
        #     "1": "#4CAF50",
        # },
        # color="Count",
        color_discrete_sequence=px.colors.qualitative.G10,
    )

    # Combine subplots into a single figure
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=[
            "Age Distribution",
            "Resting BP vs. Cholesterol",
            "Chest Pain Types",
            "Gender Distribution",
        ],
    )
    fig.add_trace(fig1["data"][0], 1, 1)
    fig.add_trace(fig2["data"][0], 1, 2)
    fig.add_trace(fig3["data"][0], 2, 1)
    fig.add_trace(fig4["data"][0], 2, 2)    
    # Update layout
    fig.update_layout(
        {"template": "plotly_white"},
        height=800,
        width=1280,
        coloraxis_showscale=False,
    )
        
    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    # Embed the HTML in the response
    response_html = f"""
    <html>
        <head>
            <title>Plotly Scatter Plot</title>
        </head>
        <body>
            {plot_html}
        </body>
    </html>
    """
    return HTMLResponse(content=response_html, status_code=200)


@app.get("/kpis")
def get_kpi():
    df = pd.read_csv("./dataset/heart.csv")
    avg_age = df["age"].mean()
    print(avg_age)
    avg_blood_pressure = df["trtbps"].mean()
    print(avg_blood_pressure)
    female_ratio = (df["sex"] == 0).mean() * 100
    print(female_ratio)
    response = {
        "average_age": avg_age,
        "average_blood_pressure": avg_blood_pressure,
        "female_ratio": female_ratio,
    }
    return response


# get_interactive_plot()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
