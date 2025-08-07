import pytest
from data.models import Laptop, create_laptop, status_enum
from pydantic import ValidationError
from datetime import datetime


def test_valid_laptop_creation():
    data = {
        "marketplace_id": "abc123",
        "title": " Acer Nitro 5 ",
        "price": "2 999,99 zł",
        "model": "Acer Nitro 5",
        "cpu": "Intel Core i5",
        "gpu": "NVIDIA GTX 1650",
        "ram": "8 GB",
        "storage": "512 GB SSD",
        "status": "Używane",
        "location": " Kraków ",
        "appearance_time": "2024-05-01T12:00:00",
        "disappearance_time": None,
        "link": "http://example.com",
        "description": "  Gaming laptop ",
    }

    laptop = create_laptop(data)

    assert isinstance(laptop, Laptop)
    assert laptop.title == "Acer Nitro 5"
    assert laptop.price == 2999.99
    assert laptop.status == status_enum.UZYWANE
    assert laptop.location == "Kraków"
    assert laptop.description == "Gaming laptop"
    assert laptop.appearance_time == datetime(2024, 5, 1, 12, 0, 0)
    assert laptop.disappearance_time is None


@pytest.mark.parametrize("bad_price", ["abc", "12..3", "1,000,000zł", None])
def test_invalid_price_raises(bad_price):
    data = {
        "title": "Test",
        "price": bad_price,
        "status": "Nowe",
        "location": "Warsaw",
        "link": "http://example.com"
    }
    with pytest.raises(ValidationError):
        create_laptop(data)


@pytest.mark.parametrize("invalid_date", ["not-a-date", "13-2024-01", 123])
def test_invalid_datetime_raises(invalid_date):
    data = {
        "title": "Test",
        "price": "1234",
        "status": "Nowe",
        "location": "Warsaw",
        "link": "http://example.com",
        "appearance_time": invalid_date
    }
    with pytest.raises(ValidationError):
        create_laptop(data)


def test_default_description_when_none():
    data = {
        "title": "HP Pavilion",
        "price": "2000",
        "status": "Nowe",
        "location": "Poznań",
        "link": "http://example.com",
        "description": None
    }

    laptop = create_laptop(data)
    assert laptop.description == "NO DESCRIPTION"


@pytest.mark.parametrize("status_value", ["Nowe", "Używane", "Uszkodzone"])
def test_valid_enum_status(status_value):
    data = {
        "title": "Laptop",
        "price": "1500",
        "status": status_value,
        "location": "Wrocław",
        "link": "http://example.com"
    }
    laptop = create_laptop(data)
    assert laptop.status.value == status_value


def test_invalid_enum_status():
    data = {
        "title": "Laptop",
        "price": "1500",
        "status": "Zepsuty",
        "location": "Wrocław",
        "link": "http://example.com"
    }
    with pytest.raises(ValidationError):
        create_laptop(data)
