import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import mpld3
import json

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
axes[1, 0].bar(cp_counts.index, cp_counts.values, color="#FFC107", edgecolor="black")
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
html_file = open("index.html", "w")
html_file.write(html_str)
html_file.close()


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
    # print(html_str)
    plot_json = json.dumps(html_str)
    # print(plot_json)
    # Send the JSON representation of the plot in the API response
    return plot_json

result = get_interactive_plot()

print(json.loads(result))
