from sqlalchemy import Column, Integer, String
import sqlalchemy
import psycopg2
import sqlalchemy.ext
import sqlalchemy.ext.declarative
import sqlalchemy.orm
from config import DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_PORT, DB_NAME

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
print(f"Connecting to database at {DB_SERVER}:{DB_PORT}...")
engine = sqlalchemy.create_engine(DATABASE_URL)

Base = sqlalchemy.ext.declarative.declarative_base()

class LaptopListing(Base):
    __tablename__  = "listings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    marketplace_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    price = Column(String, nullable=False)
    status = Column(String, nullable=False)
    location = Column(String, nullable=False)
    link = Column(String, nullable=False)
    description = Column(String, nullable=False)


Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

def add_data(data):
    """
    Adds data to the database.
    
    :param data: List of dictionaries containing laptop listings.
    """
    print(f"Adding {len(data)} items to the database...")
    for i, item in enumerate(data, start=1):
        new_listing = LaptopListing(
            marketplace_id=item['marketplace_ID'],
            title=item['title'],
            price=item['price'],
            status=item['status'],
            location=item['location'],
            link=item['link'],
            description=item['description']
        )
        session.add(new_listing)
    session.commit()
    print(f"Inserted {len(data)} items into the database successfully.")

def get_data():
    """
    Retrieves all laptop listings from the database.
    
    :return: List of dictionaries containing laptop listings.
    """
    print("Retrieving data from the database...")
    listings = session.query(LaptopListing).all()
    data = []
    for listing in listings:
        data.append({
            'marketplace_ID': listing.marketplace_id,
            'title': listing.title,
            'price': listing.price,
            'status': listing.status,
            'location': listing.location,
            'link': listing.link,
            'description': listing.description
        })
    print(f"Retrieved {len(data)} items from the database.")
    return data

def delete_data(marketplace_id):
    """
    Deletes a laptop listing from the database by marketplace ID.
    
    :param marketplace_id: The marketplace ID of the listing to delete.
    """
    print(f"Deleting listing with marketplace ID {marketplace_id} from the database...")
    listing = session.query(LaptopListing).filter_by(marketplace_id=marketplace_id).first()
    if listing:
        session.delete(listing)
        session.commit()
        print(f"Deleted listing with marketplace ID {marketplace_id} successfully.")
    else:
        print(f"No listing found with marketplace ID {marketplace_id}.")

