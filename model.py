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

app = FastAPI()

# xTest would be [[13 numeric values here...]]

# Allow all origins to access the API (replace "*" with your frontend URL in production)
origins = ["*"]

data = pd.read_csv("./dataset/heart.csv")

# Add CORS middleware to allow cross-origin requests
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
    # Set a seaborn style for better aesthetics
    sns.set(style="ticks")

    # Create a sample DataFrame (replace this with your actual dataset)
    df = pd.read_csv("./dataset/heart.csv")

    # Set up subplots
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

    # Plot 1: Age Distribution
    axes[0, 0].hist(df["age"], bins=10, color="#4CAF50", edgecolor="black")
    axes[0, 0].set_title("Age Distribution")
    axes[0, 0].set_xlabel("Age")
    axes[0, 0].set_ylabel("Frequency")

    # Plot 2: Scatter Plot of Resting Blood Pressure vs. Cholesterol
    colors = ["#E53935" if output == 1 else "#3949AB" for output in df["output"]]
    axes[0, 1].scatter(df["trtbps"], df["chol"], c=colors, edgecolor="black", alpha=0.7)
    axes[0, 1].set_title("Resting BP vs. Cholesterol")
    axes[0, 1].set_xlabel("Resting Blood Pressure")
    axes[0, 1].set_ylabel("Cholesterol")

    # Plot 3: Bar Chart of Chest Pain Types
    cp_counts = df["cp"].value_counts()
    axes[1, 0].bar(
        cp_counts.index, cp_counts.values, color="#FFC107", edgecolor="black"
    )
    axes[1, 0].set_title("Chest Pain Types")
    axes[1, 0].set_xlabel("Chest Pain Type")
    axes[1, 0].set_ylabel("Count")
    axes[1, 0].set_xticks(cp_counts.index)
    axes[1, 0].set_xticklabels(cp_counts.index)

    # Plot 4: Pie Chart of Gender Distribution
    gender_counts = df["sex"].value_counts()
    axes[1, 1].pie(
        gender_counts,
        labels=["Male", "Female"],
        colors=["#5E35B1", "#E57373"],
        autopct="%1.1f%%",
        startangle=90,
    )
    axes[1, 1].set_title("Gender Distribution")

    # Adjust layout
    plt.tight_layout()
    plt.grid(False)

    html_str = mpld3.fig_to_html(fig)
    plot_json = json.dumps(html_str)
    print(plot_json)

    # Send the JSON representation of the plot in the API response
    return plot_json

@app.get("/kpis")
def get_kpi():
    df = pd.read_csv('./dataset/heart.csv')
    avg_age = df["age"].mean()
    avg_blood_pressure = df["trtbps"].mean()
    most_occured_chest_pain_type = df['cp'].mode()
    return avg_age, avg_blood_pressure, most_occured_chest_pain_type

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
