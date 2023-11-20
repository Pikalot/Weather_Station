from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from datetime import datetime, timedelta
from supabase import create_client
import os, json, requests, random

load_dotenv()

app = Flask(__name__)

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

table_name = 'weather'
start_time = datetime.now()
last_upload_time = start_time


def fetch_data_from_database(table_name):
  response = supabase.table(table_name).select("id", "temperature", "humidity", "timestamp", count='exact').execute()

  if hasattr(response, 'data') and 'error' in response.data:
        print("Error fetching data:", response.data['error'])
        return []
    
  data = response.data[0] if response.data else None

  if data and 'temperature' in data and data['temperature'] is not None:
    data['temperature'] = format_number(data['temperature'])

  if data and 'humidity' in data and data['humidity'] is not None:
    data['humidity'] = format_number(data['humidity'])
    
  # Sort the contents by their 'id' in ascending order
  sorted_data = sorted(response.data, key=lambda x: x['timestamp'])

  return sorted_data

# Format temperature and humidity
def format_number(number):
  try:
    # Convert salary to float and format it without cents
    formatted_number = "{:.2f}".format(number)
    return formatted_number
  except (ValueError, TypeError):
    # Return the original salary if there's an issue formatting
    return number
    
# Endpoint to fetch data
@app.route('/get_data', methods=['GET'])
def get_data():
  try:
      # Fetch data from Supabase or any other source
      data = fetch_data_from_database(table_name)
      return jsonify(data)
  except Exception as e:
      print(f"Error fetching data: {e}")
      return jsonify({"error": str(e)}), 500  # Return a 500 Internal Server Error status for any errors

@app.route('/post_data_to_supabase', methods=['POST'])
def post_data_to_supabase():
    try:
        # Get data from the request
        temperature = request.json.get('temperature')
        humidity = request.json.get('humidity')

        # Data to insert
        data = {'temperature': temperature, 'humidity': humidity}

        # Insert data into the specified table
        response = supabase.table(table_name).upsert([data], returning='minimal').execute()

        # Check the response
        if response.status_code == 201:
            print('Data inserted successfully')
        else:
            print('Error inserting data:', response.content)

        return jsonify({"message": "Data inserted successfully"}), 201

    except Exception as e:
        print('Error:', e)
        return jsonify({"error": str(e)}), 500


# Interface route
@app.route('/')
def index():

  global last_upload_time
  # Retrieve data from Supabase
  weather = fetch_data_from_database(table_name)
  analyze = analyze_data(weather[-1]['temperature'])
    
  return render_template('index.html', weather=weather, analyze=analyze)

    
# Simple data analysis function
def analyze_data(temperature):
    threshold = 30.0  # Example of a high temperature
    if temperature > threshold:
        return "Temperature is high."
    else:
        return "Temperature is not high"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
