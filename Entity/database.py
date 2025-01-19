from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Utwórz silnik bazy danych

load_dotenv()
user = os.getenv('DATABASE_USER')
password = os.getenv('DATABASE_PASSWORD')
host = os.getenv('DATABASE_HOST')
database = os.getenv('DATABASE_NAME')
database_port = os.getenv('DATABASE_PORT')
DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{database_port}/{database}"
engine = create_engine(DATABASE_URL)

# Utwórz obiekt MetaData
metadata = MetaData()

# Załaduj metadane z bazy danych
metadata.reflect(bind=engine)

# Utwórz bazową klasę dla modeli
Base = declarative_base(metadata=metadata)

# Utwórz sesję
Session = sessionmaker(bind=engine)
session = Session()
