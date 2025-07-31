import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from data.models import Laptop
from data.data_manager import sync_with_database, timestamp_laptop 

@pytest.fixture
def sample_laptop():
    return Laptop(
        marketplace_id="ID123",
        title="Test Laptop",
        price="1000 zł",
        status="Nowy",
        location="Warszawa",
        link="http://test.com",
        description="Test description",
        appearance_time=None,
        disappearance_time=None,
    )

@pytest.fixture
def another_laptop():
    return Laptop(
        marketplace_id="ID456",
        title="Another Laptop",
        price="1500 zł",
        status="Używany",
        location="Kraków",
        link="http://test2.com",
        description="Another description",
        appearance_time=None,
        disappearance_time=None,
    )

@patch("data.data_manager.get_data")
@patch("data.data_manager.add_data")
@patch("data.data_manager.modify_data")
@patch("data.data_manager.logger")

def test_sync_with_database_add_new(mock_logger, mock_modify_data, mock_add_data, mock_get_data, sample_laptop):
    mock_get_data.return_value = []
    scraped = [sample_laptop]
    sync_with_database(scraped)
    mock_add_data.assert_called_once_with(scraped)
    assert scraped[0].appearance_time is not None
    mock_modify_data.assert_not_called()
    mock_logger.info.assert_any_call(f"Adding new laptop to the database: {sample_laptop.title}, ID: {sample_laptop.marketplace_id}")

@patch("data.data_manager.get_data")
@patch("data.data_manager.add_data")
@patch("data.data_manager.modify_data")
@patch("data.data_manager.logger")
def test_sync_with_database_remove_old(mock_logger, mock_modify_data, mock_add_data, mock_get_data, sample_laptop, another_laptop):
    mock_get_data.return_value = [sample_laptop]
    scraped = [another_laptop]
    sync_with_database(scraped)
    mock_add_data.assert_called_once()
    mock_modify_data.assert_called_once_with(sample_laptop.title, sample_laptop.disappearance_time)
    assert sample_laptop.disappearance_time is not None

@patch("data.data_manager.modify_data")
@patch("data.data_manager.logger")
def test_timestamp_laptop_appearance(mock_logger, mock_modify_data, sample_laptop):
    timestamp_laptop(True, sample_laptop)
    assert sample_laptop.appearance_time is not None
    mock_modify_data.assert_not_called()
    mock_logger.info.assert_any_call(f"Timestamping appearance: {sample_laptop.title}, ID: {sample_laptop.marketplace_id}")

@patch("data.data_manager.modify_data")
@patch("data.data_manager.logger")
def test_timestamp_laptop_disappearance(mock_logger, mock_modify_data, sample_laptop):
    timestamp_laptop(False, sample_laptop)
    assert sample_laptop.disappearance_time is not None
    mock_modify_data.assert_called_once_with(sample_laptop.title, sample_laptop.disappearance_time)
    mock_logger.info.assert_any_call(f"Timestamping disappearance: {sample_laptop.title}, ID: {sample_laptop.marketplace_id}")
