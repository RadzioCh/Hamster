from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import traceback
import sys


class DatabaseConnect():
    def __init__(self):
        load_dotenv()
        self.user = os.getenv('DATABASE_USER')
        self.password = os.getenv('DATABASE_PASSWORD')
        self.host = os.getenv('DATABASE_HOST')
        self.database = os.getenv('DATABASE_NAME')
        self.database_port = os.getenv('DATABASE_PORT')

        # print(f"Utworzenie połączenia z bądem danych: {self.user}:{self.password}@{self.host}:{self.database_port}/{self.database}")
        # sys.exit()

    def DbConnect(self):
        try:
            DATABASE_URL = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.database_port}/{self.database}"
            engine = create_engine(DATABASE_URL)
            Session = sessionmaker(bind=engine)
            session = Session()
            return session
        except Exception as e:
            # error_details = traceback.format_exc()  {error_details}
            print(f"Błąd podczas łączenia z bazą danych ......... ") 
            return None
        
    def DbConnectAndMetadata(self):
        try:
            DATABASE_URL = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.database_port}/{self.database}"
            engine = create_engine(DATABASE_URL)
            # Utwórz obiekt MetaData
            metadata = MetaData()
            metadata.reflect(bind=engine)
            Base = declarative_base(metadata=metadata)

            Session = sessionmaker(bind=engine)
            session = Session()
            return {"session": session, "metadata": metadata, "Base": Base}  # Zwróć obiekt session
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Błąd podczas łączenia z bazą danych: {error_details}")
            return None