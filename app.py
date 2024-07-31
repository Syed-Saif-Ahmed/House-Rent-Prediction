from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import math

app = Flask(__name__)

# Define encoding functions
def code_Residence_Type(residence_type):
    return 0 if residence_type == ('flat' or '') else (1 if residence_type == 'shared room' else 2)

def code_yes_no(value):
    return 1 if value == 'Yes' else 0


@app.route('/')
def home():
    residence_options = ['','flat', 'shared room', 'individual house']
    bathroom_options = ['','Yes', 'No']
    kitchen_options = ['','Yes', 'No']
    shopping_options = ['','Yes', 'No']
    transport_options = ['','Yes', 'No']
    medical_options = ['','Yes', 'No']
    playground_options = ['','Yes', 'No']

    return render_template(
        'index.html',
        Residence=residence_options,
        bathroom=bathroom_options,
        kitchens=kitchen_options,
        Shopping=shopping_options,
        Transport=transport_options,
        Medical=medical_options,
        Playground=playground_options
    )

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input from the form
        user_input = {
            'Residence_Type': request.form['residence_type'], # 
            'Residence_Score':0,
            'Attached_bathroom': request.form['attached_bathroom'], #
            'attached_kitchens': request.form['attached_kitchens'], #
            'avl_shoopingmall': request.form['avl_shoopingmall'], #
            'avl_transport_facility_colllege': request.form['avl_transport_facility_colllege'], #
            'avl_medical': request.form['avl_medical'], #
            'avl_fooding': int(request.form['avl_fooding']),
            'avl_transport_market_time': int(request.form['avl_transport_market_time']),
            'transport_time': int(request.form['transport_time']),
            'avl_play_ground': request.form['avl_play_ground'] #
        }

        # Process user input
        user_input['Residence_Type'] = code_Residence_Type(user_input['Residence_Type'])
        user_input['Attached_bathroom'] = code_yes_no(user_input['Attached_bathroom'])
        user_input['attached_kitchens'] = code_yes_no(user_input['attached_kitchens'])
        user_input['avl_shoopingmall'] = code_yes_no(user_input['avl_shoopingmall'])
        user_input['avl_transport_facility_colllege'] = code_yes_no(user_input['avl_transport_facility_colllege'])
        user_input['avl_medical'] = code_yes_no(user_input['avl_medical'])
        user_input['avl_play_ground'] = code_yes_no(user_input['avl_play_ground'])
        # Convert user input to DataFrame

        user_input_df = pd.DataFrame([user_input])

        # Load the best model from the pickle file
        loaded_best_model = joblib.load('best_model.pkl')


        # Predict the house rent based on user input
        prediction = loaded_best_model.predict(user_input_df)[0]

        # Round up to the nearest thousand
        rounded_prediction = math.ceil(prediction / 1000) * 1000

        # Return prediction
        return jsonify(prediction=str(rounded_prediction))
    except Exception as e:
        # Return error message
        return jsonify(error=str(e))

@app.route('/favicon.ico')
@app.route('/favicon.png')
def favicon():
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
