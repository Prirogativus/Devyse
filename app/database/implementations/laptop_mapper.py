from data.models import Laptop
from data.db_models import LaptopListing

def laptop_to_db(laptop: Laptop) -> LaptopListing:
    return LaptopListing(
        marketplace_id=laptop.marketplace_id,
        title=laptop.title,
        price=laptop.price,
        model=laptop.model,
        cpu=laptop.cpu,
        gpu=laptop.gpu,
        ram=laptop.ram,
        storage=laptop.storage,
        status=laptop.status.value if hasattr(laptop.status, "value") else laptop.status,
        location=laptop.location,
        appearance_time=laptop.appearance_time,
        disappearance_time=laptop.disappearance_time,
        link=laptop.link,
        description=laptop.description
    )

def db_to_laptop(listing: LaptopListing) -> Laptop:
    return Laptop(
        marketplace_id=listing.marketplace_id,
        title=listing.title,
        price=listing.price,
        model=listing.model,
        cpu=listing.cpu,
        gpu=listing.gpu,
        ram=listing.ram,
        storage=listing.storage,
        status=listing.status,
        location=listing.location,
        appearance_time=listing.appearance_time,
        disappearance_time=listing.disappearance_time,
        link=listing.link,
        description=listing.description
    )