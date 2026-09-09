import requests
import pandas as pd
from sqlalchemy import create_engine
import logging
import os

# ============================================
# SET UP LOGGING
# ============================================
os.makedirs('../logs', exist_ok=True)

logging.basicConfig(
    filename='../logs/api_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Pipeline started")
print("Logging setup complete")

# ============================================
# EXTRACT - Fetch Data from API
# ============================================
def extract_data(cities):
    """Fetch weather data from Open-Meteo API"""
    all_data = []
    for city in cities:
      print(f"Fetching data from API for city: {city['name']}")
      url = f"https://api.open-meteo.com/v1/forecast?latitude={city['lat']}&longitude={city['lon']}&current_weather=true"
    
      print(f"Fetching data from API for city: {city['name']}")
      response = requests.get(url)
    
      if response.status_code == 200:
        data = response.json()
        data['city'] = city['name'] # Add city information to the data
        all_data.append(data)
        logging.info("API data fetched successfully")
        print(f"API data fetched successfully for city: {city['name']}")
      else:
        print(f"API request failed for city: {city['name']}")

    print(f"Total cities fetched: {len(all_data)}")
    return all_data

# ============================================
def transform_data(data):
    """Extract relevant fields from JSON response"""
    city = data['city']
    current = data['current_weather']

    df = pd.DataFrame([{
        'city': city,
        'temperature': current['temperature'],
        'windspeed': current['windspeed'],
        'humidity': current.get('humidity', None),  # Assuming humidity might be present
        'pressure': current.get('pressure', None),  # Assuming pressure might be present
        'rain': current.get('rain', None),  # Assuming rain might be present
        'cloudcover': current.get('cloudcover', None),  # Assuming cloud cover might be present
        'observation_time': current['time']

    }])
    
    logging.info(f"Data transformed successfully. Rows: {len(df)}")
    print(f"✅ Transformed data for {city}: {current['temperature']}°C, Wind: {current['windspeed']} km/h")
    return df

# ============================================
# LOAD - Write to PostgreSQL
# ============================================
def load_data(df):
    """Load data to PostgreSQL using append mode"""
    password = "Hoangbaongoc140906!"
    engine = create_engine(f"postgresql://postgres:{password}@localhost:5433/data_projects")
    
    df.to_sql('weather_data_v2', engine, if_exists='append', index=False)
    
    logging.info(f"Data loaded successfully. Rows: {len(df)}")
    print(f"Loaded {len(df)} rows to PostgreSQL")


# ============================================
# RUN PIPELINE
# ============================================
def run_pipeline():
    print("=" * 50)
    print("STARTING WEATHER API PIPELINE")
    print("=" * 50)

    cities = [
        {'name': 'Siliguri', 'lat': 26.7, 'lon': 88.4},
        {'name': 'Delhi', 'lat': 28.6, 'lon': 77.2},
        {'name': 'Mumbai', 'lat': 19.1, 'lon': 72.9},
        {'name': 'Bangalore', 'lat': 12.9, 'lon': 77.6},
    ]
    
    all_data = extract_data(cities)
    for city_data in all_data:
        df = transform_data(city_data)
        load_data(df)
    
    print("=" * 50)
    print("PIPELINE COMPLETE!")
    print("=" * 50)
    logging.info("Pipeline executed successfully")

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    run_pipeline()