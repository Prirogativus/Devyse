import pytest
from data.database_connector import get_data, LaptopListing, add_data, modify_data
from unittest.mock import MagicMock, patch
from data.models import Laptop
from datetime import datetime


@pytest.fixture
def sample_laptop():
    return Laptop(
        marketplace_id="123",
        title="Lenovo ThinkPad",
        price="1500",
        status="active",
        location="Warsaw",
        link="http://example.com",
        description="Test laptop",
        appearance_time=datetime(2024, 1, 1),
        disappearance_time=None
    )


def test_add_data(sample_laptop):
    with patch("data.database_connector.session") as mock_session:
        add_data([sample_laptop])

        assert mock_session.add.called
        assert mock_session.commit.called


def test_get_data():
    mock_laptop_listing = MagicMock(spec=LaptopListing)
    mock_laptop_listing.marketplace_id = "001"
    mock_laptop_listing.title = "Dell XPS"
    mock_laptop_listing.price = "3000"
    mock_laptop_listing.status = "active"
    mock_laptop_listing.location = "Krakow"
    mock_laptop_listing.link = "http://example.com"
    mock_laptop_listing.description = "Powerful laptop"
    mock_laptop_listing.appearance_time = datetime(2024, 1, 1)
    mock_laptop_listing.disappearance_time = None

    with patch("data.database_connector.session") as mock_session:
        mock_session.query.return_value.all.return_value = [mock_laptop_listing]

        result = get_data()

        assert len(result) == 1
        assert isinstance(result[0], Laptop)
        assert result[0].title == "Dell XPS"


def test_modify_data_add_disappearance():
    mock_listing = MagicMock()
    mock_listing.disappearance_time = None
    mock_listing.title = "HP Envy"

    with patch("data.database_connector.session") as mock_session:
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_listing

        now = datetime(2024, 2, 2)

        modify_data("HP Envy", now)

        assert mock_listing.disappearance_time == now
        assert mock_session.commit.called


def test_modify_data_already_set():
    mock_listing = MagicMock()
    mock_listing.disappearance_time = datetime(2024, 1, 1)
    mock_listing.title = "HP Envy"

    with patch("data.database_connector.session") as mock_session:
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_listing

        modify_data("HP Envy", datetime(2024, 2, 2))

        assert not mock_session.commit.called
