from data_science.modelling import SimpleModel
import pandas as pd

model = SimpleModel()

model.load(model_folder="/models")

request_dict = {
        "idx": 150000,
        "features": {
            "attr_a": 1,
            "attr_b": "c",
            "scd_a": 0.55,
            "scd_b": 3
        }
}

df_features = pd.json_normalize(request_dict["features"])

predicted_label = model.predict(features = df_features)

print(predicted_label)