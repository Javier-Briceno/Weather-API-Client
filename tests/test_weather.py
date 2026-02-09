import pytest
import json
import os
from weather_fetcher import get_weather, format_output, load_mock_data

class TestMockDataLoading:
    def test_load_valid_mock_data(self):
        mock_path = "mocks/sunny_berlin.json"
        if os.path.exists(mock_path):
            data = load_mock_data(mock_path)
            assert "location" in data
            assert "current" in data
    
    def test_load_invalid_mock_data(self):
        with pytest.raises(SystemExit):
            load_mock_data("mocks/non_existent_file.json")
            
class TestWeatherDataParsing:
    def test_get_weather_with_mock_data(self):
        mock_path = "mocks/sunny_berlin.json"
        
        if os.path.exists(mock_path):
            weather = get_weather(
                city="Berlin",
                units="metric",
                mock_path=mock_path
            )
            
            assert "city" in weather
            assert "temperature" in weather
            assert "humidity" in weather
            assert "condition" in weather
            assert weather["units"] == "metric"

    def test_units_metric(self):
        mock_path = "mocks/sunny_berlin.json"
        
        if os.path.exists(mock_path):
            if os.path.exists(mock_path):
                weather = get_weather(
                    city="Berlin",
                    units="metric",
                    mock_path=mock_path
                )
                
                assert weather["units"] == "metric"
                # Temperature should be in reasonable Celsius range
                assert -50 <= weather["temperature"] <= 60
                
    def test_units_imperial(self):
        mock_path = "mocks/sunny_berlin.json"
        
        if os.path.exists(mock_path):
            weather = get_weather(
                city="Berlin",
                units="imperial",
                mock_path=mock_path
            )
            
            assert weather["units"] == "imperial"
            # Temperature should be in reasonable Fahrenheit range
            assert -60 <= weather["temperature"] <= 140

class TestOutputFormatting:
    def test_format_output_metric(self):
        weather = {
            "city": "Berlin",
            "temperature": 20.5,
            "humidity": 65,
            "condition": "Sunny",
            "units": "metric"
        }
        
        output = format_output(weather)
        assert "Berlin" in output
        assert "20.5°C" in output
        assert "65%" in output
        assert "Sunny" in output
        
    def test_format_output_imperial(self):
        weather = {
            "city": "New York",
            "temperature": 68.9,
            "humidity": 74,
            "condition": "Clear",
            "units": "imperial"
        }
        
        output = format_output(weather)
        assert "New York" in output
        assert "68.9°F" in output
        assert "74%" in output
        assert "Clear" in output