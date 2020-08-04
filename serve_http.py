"""
Script for serving.
"""
from flask import current_app, Flask, request
import pandas as pd
import numpy as np
from tensorflow.keras import models

OUTPUT_MODEL_NAME = "/artefact/bdrk-model/model_COVID_bdrk.h5"

# pylint: disable=invalid-name
app = Flask(__name__)


@app.before_first_request
def init_background_threads():
    """Instantiate the Tensorflow model before the first request.
    """
    current_app.model = models.load_model(OUTPUT_MODEL_NAME)


@app.route("/", methods=["POST"])
def predict():
    df = pd.read_csv(request.files.get('file'))
    y_pred = pd.DataFrame(current_app.model.predict(df))
    y_pred[y_pred < 0] = 0
    y_pred.columns = ['beyond_minus6.0H', 'minus6.0_to_5.75H',
                      'minus5.75_to_5.5H', 'minus5.5_to_5.25H',
                      'minus5.25_to_5.0H', 'minus5.0_to_4.75H',
                      'minus4.75_to_4.5H', 'minus4.5_to_4.25H',
                      'minus4.25_to_4.0H', 'minus4.0_to_3.75H',
                      'minus3.75_to_3.5H', 'minus3.5_to_3.25H',
                      'minus3.25_to_3.0H', 'minus3.0_to_2.75H',
                      'minus2.75_to_2.5H', 'minus2.5_to_2.25H',
                      'minus2.25_to_2.0H', 'minus2.0_to_1.75H',
                      'minus1.75_to_1.5H', 'minus1.5_to_1.25H',
                      'minus1.25_to_1.0H', 'minus1.0_to_0.75H',
                      'minus0.75_to_0.5H', 'minus0.5_to_0.25H',
                      'minus0.25_to_0H']

    return y_pred.to_json()


def main():
    """Starts the Http server"""
    app.run()


if __name__ == "__main__":
    main()
