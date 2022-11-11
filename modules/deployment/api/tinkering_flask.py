import flask
from flask import Flask, jsonify, request
from data_science.modelling import SimpleModel
import pandas as pd

model = SimpleModel()
model.load(model_folder="/models")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Hello, DareData :)'

@app.route('/predict', methods=['POST'])
def predict():
    request_dict = request.get_json()

    print(type(request_dict))

    # request_dict = {
    #     "idx": 150000,
    #     "features": {
    #         "attr_a": 1,
    #         "attr_b": "c",
    #         "scd_a": 0.55,
    #         "scd_b": 3
    #     }
    # }

    df_features = pd.json_normalize(request_dict["features"])

    predicted_label = model.predict(features = df_features)

    return str(predicted_label)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')