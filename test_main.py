import pytest
from main import fetch_data_from_database, format_number, analyze_data
from dotenv import load_dotenv
from supabase import create_client
import os, json, requests, random


supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

table_name = 'sample_table'

@pytest.fixture
def sample_data():
    # Sample weather data for testing
    return [
        {'id': 1, 'temperature': 21.28, 'humidity': 64.47, 'timestamp': '2023-11-20T06:33:34.795555+00:00'},
        {'id': 2, 'temperature': 14.1, 'humidity': 50, 'timestamp': '2023-11-20T06:34:06.603443+00:00'},
    ]


def test_fetch_data_from_database(sample_data):
    # Test that the fetch_data_from_database function returns the expected data
    result = fetch_data_from_database(table_name)
  
    # Convert data types in the result list to match sample_data
    converted_result = [
      {
          "id": item["id"],
          "temperature": float(item["temperature"]),
          "humidity": float(item["humidity"]),
          "timestamp": item["timestamp"],
      }
      for item in result
    ]

    # Print result and sample_data for debugging
    print("Result:", result)
    print("Sample Data:", sample_data)
  
    # Check if each item in sample_data is present in result
    for expected_item in sample_data:
        assert expected_item in converted_result

      

def test_format_number():
    # Test the format_number function with a sample number
    formatted_number = format_number(25.456)
    assert formatted_number == '25.46'  # Assuming you want two decimal places

def test_analyze_data_high_temperature():
    # Test analyze_data function with a high temperature
    result = analyze_data(35.0)
    assert result == "Temperature is high."

def test_analyze_data_low_temperature():
    # Test analyze_data function with a low temperature
    result = analyze_data(20.0)
    assert result == "Temperature is not high"
