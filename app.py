from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your Edamam API credentials (replace with your actual API keys)
APP_ID = 'your_edamam_app_id'
APP_KEY = 'your_edamam_app_key'

# Endpoint URL for the Edamam Food API
NUTRITION_URL = 'https://api.edamam.com/api/food-database/v2/nutrients'

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        food_item = request.form['food_item']
        nutrition_data = get_nutrition_data(food_item)
        return render_template('index.html', nutrition_data=nutrition_data, food_item=food_item)
    return render_template('index.html', nutrition_data=None)

# Function to fetch nutrition data from Edamam API
def get_nutrition_data(food_item):
    headers = {
        'Content-Type': 'application/json'
    }

    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'ingr': food_item
    }

    # Making the API request
    response = requests.post(NUTRITION_URL, json=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'totalNutrients' in data:
            return data['totalNutrients']
        else:
            return {"error": "No nutrition data available for this item."}
    else:
        return {"error": "Error fetching data from the API."}

if __name__ == '__main__':
    app.run(debug=True)
