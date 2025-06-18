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
    title = Column(String, nullable=False)
    price = Column(String, nullable=False)
    status = Column(String, nullable=False)
    location = Column(String, nullable=False)
    link = Column(String, nullable=False)
    description = Column(String, nullable=False)

print("Creating tables if they don't exist...")
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
            title=item['title'],
            price=item['price'],
            status=item['status'],
            location=item['location'],
            link=item['link'],
            description=item['description']
        )
        session.add(new_listing)

        if i % 10 == 0:
            print(f"{i} items prepared for insertion...")

    session.commit()
    print(f"Inserted {len(data)} items into the database successfully.")

def main():
    print("Script started. No action in main yet.")

if __name__ == "__main__":
    main()
