import pytest
from unittest.mock import patch, MagicMock

from tools.weather import get_weather


@patch("tools.weather.urllib.request.urlopen")
def test_get_weather(mock_urlopen):
    geocoding_response = MagicMock()
    geocoding_response.__enter__.return_value = geocoding_response

    weather_response = MagicMock()
    weather_response.__enter__.return_value = weather_response

    mock_urlopen.side_effect = [
        geocoding_response,
        weather_response,
    ]

    with patch("tools.weather.json.load") as mock_json_load:
        mock_json_load.side_effect = [
            {
                "results": [
                    {
                        "name": "Jakarta",
                        "country": "Indonesia",
                        "latitude": -6.2,
                        "longitude": 106.8,
                    }
                ]
            },
            {
                "current": {
                    "temperature_2m": 25.1,
                    "apparent_temperature": 29.3,
                    "weather_code": 3,
                }
            },
        ]

        result = get_weather("Jakarta")

    assert result == {
        "city": "Jakarta",
        "country": "Indonesia",
        "temperature": 25.1,
        "apparent_temperature": 29.3,
        "weather_code": 3,
    }


@patch("tools.weather.urllib.request.urlopen")
def test_get_weather_city_not_found(mock_urlopen):
    geocoding_response = MagicMock()
    geocoding_response.__enter__.return_value = geocoding_response

    mock_urlopen.return_value = geocoding_response

    with patch("tools.weather.json.load") as mock_json_load:
        mock_json_load.return_value = {
            "results": []
        }

        with pytest.raises(ValueError, match="City not found"):
            get_weather("NotARealCity123")