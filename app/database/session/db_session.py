import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.db_models import Base
from config.constants_manager import DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_PORT, DB_NAME

logger = logging.getLogger(__name__)

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
logger.info(f"Connecting to database at {DB_SERVER}:{DB_PORT}...")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables if they do not exist
Base.metadata.create_all(engine)