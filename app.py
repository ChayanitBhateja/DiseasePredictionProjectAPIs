# from flask import Flask, send_file
# import io
# import matplotlib.pyplot as plt

# app = Flask(__name__)


# @app.route("/plot", methods=["GET"])
# def get_plot():
#     # Create a Matplotlib plot
#     fig, ax = plt.subplots()
#     ax.plot([1, 2, 3, 4], [10, 5, 20, 15])

#     # Save the plot to a BytesIO object
#     img_buf = io.BytesIO()
#     plt.savefig(img_buf, format="png")
#     img_buf.seek(0)
#     plt.close()

#     # Send the plot as an image in the API response
#     return send_file(img_buf, mimetype="image/png")


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, jsonify
import plotly
import plotly.graph_objects as go
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/interactive_plot", methods=["GET"])
def get_interactive_plot():
    # Create a Plotly plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 5, 20, 15], mode="lines+markers"))

    # Convert the plot to JSON
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Send the JSON representation of the plot in the API response
    return jsonify(plot_json)


if __name__ == "__main__":
    app.run(debug=True)
