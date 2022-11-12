from flask import Flask, jsonify, request
from data_science.modelling import SimpleModel
import pandas as pd

# load ML model to memory
model = SimpleModel()
model.load(model_folder="/models")

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "Hello, DareData :)"


@app.route("/predict", methods=["POST"])
def predict():
    """Process API prediction request."""
    # process request features
    request_dict = request.get_json()
    df_features = pd.json_normalize(request_dict["features"])

    # make prediction
    predicted_label = model.predict(features=df_features)

    return_dict = {"prediction": str(predicted_label)}

    return jsonify(return_dict)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
