from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Load the model and column names
with open('titanic.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('columns.json', 'r') as columns_file:
    columns = json.load(columns_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print("Received data:", data)  # Log the received data
    Pclass = data['Pclass']
    Age = data['Age']
    Sex = 1 if data['Sex'] == 'female' else 0  # Convert to 1 if female, else 0
    SibSp = data['SibSp']
    Fare = data['Fare']

    # Prepare input for model
    x = np.array([Pclass, Age, Sex, SibSp, Fare]).reshape(1, -1)
    print("Input shape:", x.shape)
    prediction = model.predict(x)[0]
    return jsonify({'survived': int(prediction)})


if __name__ == '__main__':
    app.run(debug=True)
