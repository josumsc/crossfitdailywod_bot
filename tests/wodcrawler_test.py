import pytest
import requests
from bs4 import BeautifulSoup
from unittest.mock import patch, Mock
from wodcrawler import WODCrawler

@pytest.fixture
def wodcrawler():
    return WODCrawler("http://example.com")

def test_wodcrawler_initialization(wodcrawler):
    assert wodcrawler.url == "http://example.com"
    assert wodcrawler.wods == {}

@patch("requests.get")
def test_download_crossfit_wods_success(mock_get, wodcrawler):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = """
    <div class="content-container">
        <h3>Friday 20240110</h3>
        <div class="col-sm-6">Workout details for 2024-01-10</div>
    </div>
    <div class="content-container">
        <h3>Saturday 20240111</h3>
        <div class="col-sm-6">Workout details for 2024-01-11</div>
    </div>
    """
    mock_get.return_value = mock_response

    wods = wodcrawler.download_crossfit_wods()
    assert len(wods) == 2
    assert wods["20240110"] == "Workout details for 2024-01-10"
    assert wods["20240111"] == "Workout details for 2024-01-11"

@patch("requests.get")
def test_download_crossfit_wods_failure(mock_get, wodcrawler):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(Exception, match="Failed to fetch page: 404"):
        wodcrawler.download_crossfit_wods()

@patch("requests.get")
def test_download_crossfit_wods_cached(mock_get, wodcrawler):
    wodcrawler.wods = {
        "20240110": "Cached workout details for 2024-01-10"
    }

    wods = wodcrawler.download_crossfit_wods()
    assert len(wods) == 1
    assert wods["20240110"] == "Cached workout details for 2024-01-10"
    mock_get.assert_not_called()

    @patch("requests.get")
    def test_download_crossfit_wods_no_content(mock_get, wodcrawler):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = """
        <div class="content-container">
            <h3>Friday 20240110</h3>
            <div class="col-sm-6"></div>
        </div>
        """
        mock_get.return_value = mock_response

        wods = wodcrawler.download_crossfit_wods()
        assert len(wods) == 1
        assert wods["20240110"] == ""

    @patch("requests.get")
    def test_download_crossfit_wods_404(mock_get, wodcrawler):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match="Failed to fetch page: 404"):
            wodcrawler.download_crossfit_wods()
