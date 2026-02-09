"""
Weather API Client
Fetches current weather data from WeatherAPI.com with support for offline mocking and caching.
"""

import sys
import os
import argparse
import requests
import json
from dotenv import load_dotenv

def save_to_cache(data: dict, cache_path: str = "cache.json") -> None:
    # Save weather data to cache file
    with open(cache_path, "w") as f: # if doesn't exist it creates the file in same folder
        json.dump(data, f, indent=2) # overwrites file with last fetched data
        
def load_mock_data(mock_path: str) -> dict:
    #Load mock weather data from JSON file
    if not os.path.exists(mock_path): # checking if the file is found
        sys.exit(f"Error: Mock file '{mock_path}' not found")
        
    try:
        with open(mock_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"Error: Invalid JSON in mock file: {e}")
        
def fetch_from_api(city: str, api_key: str) -> dict:
    #Fetch weather data from WeatherAPI.com
    url: str = "https://api.weatherapi.com/v1/current.json"
    params: dict = {"key": api_key, "q": city}    # query parameters for API request
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check if API returned an error
        if "error" in data:
            sys.exit(f"API Error: {data['error']['message']}")
            
        return data
        
    except requests.exceptions.Timeout:
        sys.exit("Error: Request timeout - server took too long to respond")
    except requests.exceptions.HTTPError as e:
        sys.exit(f"HTTP Error {e.response.status_code}: {e.response.text[:200]}")
    except requests.exceptions.RequestException as e:
        sys.exit(f"Request error: {e}")
    except json.JSONDecoder as e:
        sys.exit(f"Error parsing API response: {e}")
        
def get_weather(city: str, units: str = "metric", mock_path: str = None, api_key: str = None) -> dict:
    """
    Get weather data either from API or mock file.
    
    Args:
        city: City name to query
        units: 'metric' (Celsius) or 'imperial' (Fahrenheit)
        mock_path: Optional path to mock JSON file
        api_key: WeatherAPI key (required if not using mock)
    
    Returns:
        Dictionary with weather data
    """
    # Use mock data if provided
    if mock_path:
        data = load_mock_data(mock_path)
        
        # Warn if city name doesn't match
        mock_city = data['location']['name']
        if city.lower() != mock_city.lower():
            print(f"Note: Using mock data for '{mock_city}' (requested '{city}')")
        
        city = mock_city
    else: 
        # Fetch from API
        if not api_key:
            sys.exit("Error: WEATHER_KEY not set in .env file")
        
        data = fetch_from_api(city, api_key)
        
    # Extract relevant data
    return {
        "city": data["location"]["name"],
        "temperature": float(data["current"]["temp_c" if units == "metric" else "temp_f"]),
        "humidity": int(data["current"]["humidity"]),
        "condition": data["current"]["condition"]["text"],
        "units": units,
        "raw_data": data  # Keep raw data for caching
    }

def format_output(weather: dict) -> str:
    # Format weatehr data for display
    temp_unit = "°C" if weather["units"] == "metric" else "°F"
    return (
        f"{weather['city']}: "
        f"{weather['temperature']:.1f}{temp_unit}, "
        f"{weather['humidity']}% humidity, "
        f"{weather['condition']}"
    )
    
def main():
    # Main entry point for the weather fetcher CLI
    parser = argparse.ArgumentParser(
        description="Fetch current weather data from WeatherAPI.com",
        formatter_class=argparse.RawDescriptionHelpFormatter, # to preserve formatting of epilog
        epilog="""
Examples:
  %(prog)s Berlin
  %(prog)s "New York" --units imperial
  %(prog)s Tokyo --mock mocks/sunny_berlin.json
  %(prog)s London --save
        """ # %(prog)s will be replaced with the program name in real usage
    )
    
    parser.add_argument(
        "city",
        help="City name to query"
    )
    
    parser.add_argument(
        "--units",
        choices=["metric", "imperial"],
        default="metric",
        help="Units for temperature (default: metric)"
    )
    
    parser.add_argument(
        "--mock",
        metavar="PATH",
        help="Use mock JSON file instead of API call"
    )
    
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save response to cache.json"
    )
    
    args = parser.parse_args()
    
    # Load API key from .env
    api_key = None
    if not args.mock:
        load_dotenv()
        api_key = os.getenv("WEATHER_KEY")
    
    # Get weather data
    weather = get_weather(args.city, args.units, args.mock, api_key)
    
    # Save to cache if requested
    if args.save:
        save_to_cache(weather["raw_data"])
        print("Saved to cache.json")
        
    # Print formatted output
    print(format_output(weather))
    
if __name__ == "__main__":
    main()
