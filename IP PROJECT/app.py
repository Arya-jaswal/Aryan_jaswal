from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load the model
model = joblib.load('model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        age = float(request.form['age'])
        avg_glucose_level = float(request.form['avg_glucose_level'])
        bmi = float(request.form['bmi'])
        gender = request.form['gender']
        hypertension = request.form['hypertension']
        heart_disease = request.form['heart_disease']
        ever_married = request.form['ever_married']
        work_type = request.form['work_type']
        residence_type = request.form['Residence_type']
        smoking_status = request.form['smoking_status']

        # Convert categorical variables to numerical
        gender_num = 1 if gender == 'Male' else 0
        hypertension_num = 1 if hypertension == 'Yes' else 0
        heart_disease_num = 1 if heart_disease == 'Yes' else 0
        ever_married_num = 1 if ever_married == 'Yes' else 0
        work_type_map = {'Private': 0, 'Self-employed': 1, 'Govt_job': 2}
        work_type_num = work_type_map.get(work_type, -1)
        residence_type_num = 1 if residence_type == 'Urban' else 0
        smoking_status_map = {'formerly smoked': 0, 'never smoked': 1, 'smokes': 2, 'unknown': 3}
        smoking_status_num = smoking_status_map.get(smoking_status, -1)

        # Validate input values
        if work_type_num == -1 or smoking_status_num == -1:
            raise ValueError("Invalid work_type or smoking_status")

        # Make prediction
        prediction = model.predict([[age, avg_glucose_level, bmi, gender_num, hypertension_num, heart_disease_num, ever_married_num,
                                     work_type_num, residence_type_num, smoking_status_num]])

        # Pass the prediction result and input data to result.html
        return render_template('result.html', prediction=prediction[0], age=age, avg_glucose_level=avg_glucose_level, 
                               bmi=bmi, gender=gender, hypertension=hypertension, heart_disease=heart_disease, 
                               ever_married=ever_married, work_type=work_type, residence_type=residence_type, 
                               smoking_status=smoking_status)
    except (ValueError, KeyError) as e:
        error_message = "Error processing form data: " + str(e)
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
