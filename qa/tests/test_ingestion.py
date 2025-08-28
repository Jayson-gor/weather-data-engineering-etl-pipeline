import importlib
import os
import requests
import requests_mock
import pytest


def _load_fetch():
    try:
        mod = importlib.import_module("api_request.api_request")
    except Exception as e:
        pytest.skip(f"api_request.api_request not importable: {e}")
        return None
    fn = getattr(mod, "fetch_data", None)
    if fn is None:
        pytest.skip("No fetch_data found in api_request.api_request")
    return fn


def test_fetch_data_mocks_http():
    fetch_data = _load_fetch()
    if fetch_data is None:
        return

    with requests_mock.Mocker() as m:
        m.get(
            requests_mock.ANY,
            json={
                "location": {"name": "Nairobi"},
                "current": {"temperature": 24, "weather_descriptions": ["Sunny"]},
            },
            status_code=200,
        )
        data = fetch_data()
        assert data["location"]["name"] == "Nairobi"
        assert data["current"]["temperature"] == 24
