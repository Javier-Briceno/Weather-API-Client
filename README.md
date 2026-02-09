# Weather API Client ☁️

> A Python CLI tool for fetching current weather data with API integration, offline mocking, and caching support.

**Personal Project** | Python CLI Application

---

## 🎯 Overview

A command-line weather client that demonstrates API integration, error handling, and testing best practices. Supports both live API calls to WeatherAPI.com and offline mock data for development and testing.

**Key Features:**
- Real-time weather data fetching from WeatherAPI
- Offline mock mode for testing without API calls
- Response caching for debugging and replay
- Comprehensive error handling
- Metric and Imperial unit support
- Clean CLI interface with argparse

---

## 🛠️ Tech Stack

- **Python 3.10+** - Core language
- **Requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management
- **argparse** - Command-line argument parsing
- **pytest** - Testing framework

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Javier-Briceno/Weather-API-Client.git
cd Weather-API-Client
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API key

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your WeatherAPI key:

```env
WEATHER_KEY=your_api_key_here
```

Get a free API key at [WeatherAPI.com](https://www.weatherapi.com/)

---

## 🚀 Usage

### Basic Commands

```bash
# Get weather for a city (metric/Celsius by default)
python weather_fetcher.py Berlin

# Use Imperial units (Fahrenheit)
python weather_fetcher.py "New York" --units imperial

# Use offline mock data
python weather_fetcher.py Tokyo --mock mocks/sunny_berlin.json

# Save API response to cache.json
python weather_fetcher.py London --save

# Combine options
python weather_fetcher.py Paris --units metric --save
```

### Expected Output

```
Berlin: 18.5°C, 62% humidity, Partly cloudy
```

---

## 🏗️ Project Structure

```
Weather-API-Client/
├── weather_fetcher.py    # Main application
├── requirements.txt      # Dependencies
├── .env.example          # Environment template
├── .gitignore
├── README.md
├── mocks/                # Mock data for testing
│   ├── fog_lima.json
│   ├── rain_tokyo.json
│   ├── snow_zurich.json
│   ├── sunny_berlin.json
│   └── thunderstorm_miami.json
└── tests/
    └── test_weather.py   # Unit tests
```

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=weather_fetcher tests/

# Verbose output
pytest -v
```

**Test Coverage:**
- Mock data loading
- API data parsing
- Unit conversion (metric/imperial)
- Output formatting
- Error handling

---

## 🔧 Features in Detail

### API Integration

Fetches real-time weather data from WeatherAPI.com:
- Temperature (Celsius/Fahrenheit)
- Humidity percentage
- Weather condition text

### Mock Mode

Supports offline testing with JSON mock files:

```json
{
  "location": { "name": "Berlin" },
  "current": {
    "temp_c": 18.5,
    "temp_f": 65.3,
    "humidity": 62,
    "condition": { "text": "Partly cloudy" }
  }
}
```

### Caching

Save API responses for debugging:

```bash
python weather_fetcher.py Munich --save
# Creates cache.json with full API response
```

### Error Handling

Robust error handling for:
- Network timeouts
- Invalid API keys
- HTTP errors (4xx/5xx)
- Malformed JSON responses
- City not found
- Invalid mock files

---

## 💡 Design Decisions

### Why argparse over regex?

- **Industry standard** for Python CLI tools
- **Flexible flag ordering** (--save --units vs --units --save)
- **Automatic help generation** (--help flag)
- **Type validation** built-in
- **Easier to maintain and extend**

### Why mock files?

- Enable testing without API calls
- Avoid rate limits during development
- Test error scenarios (fog, thunderstorm, etc.)
- Faster test execution
- Reproducible test environments

### Separation of concerns

- `fetch_from_api()` - HTTP/API logic
- `load_mock_data()` - File I/O
- `get_weather()` - Business logic
- `format_output()` - Presentation
- `main()` - CLI interface

---

## 🎓 Skills Demonstrated

**For Data Engineering:**
- ✅ API data extraction (REST)
- ✅ Error handling in data pipelines
- ✅ Mock data for testing
- ✅ Environment variable configuration
- ✅ Data caching mechanisms
- ✅ CLI tool development
- ✅ Unit testing with pytest

**Software Engineering:**
- Clean code architecture
- Separation of concerns
- Comprehensive error handling
- Documentation
- Testing best practices

---

## 📈 Potential Enhancements

Future improvements could include:
- [ ] Multi-city batch queries
- [ ] Historical weather data
- [ ] Weather forecast (7-day)
- [ ] Output to CSV/JSON files
- [ ] Configuration file support
- [ ] Weather alerts and warnings
- [ ] Integration with other weather APIs

---

## 📝 License

Personal educational project.

---

## 🔗 Related Projects

- [SQL Learning Platform](https://github.com/Javier-Briceno/SQL-Learning-Platform) - Full-stack educational app
- [CS50P Todo Manager](https://github.com/Javier-Briceno/CS50P-Todo-Manager) - CLI task manager

---