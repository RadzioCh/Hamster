from Database.DatabaseConnect import DatabaseConnect
from sqlalchemy import Column, LargeBinary
from pgvector.sqlalchemy import Vector

class Models():
    def createModels(self):
        databaseConnect = DatabaseConnect()
        databaseInfo = databaseConnect.DbConnectAndMetadata()

        metadata = databaseInfo["metadata"]
        Base = databaseInfo["Base"]

        # Przejdź przez wszystkie tabele w metadanych i utwórz modele
        for table_name, table in metadata.tables.items():
            # Utwórz klasę modelu
            class_name = table_name.capitalize()
            columns = {column.name: column for column in table.columns}

            # Specjalne traktowanie kolumny embedding
            if 'embedding' in columns:
                # columns['embedding'] = Column(LargeBinary)  # Upewnij się, że embedding jest prawidłowo zdefiniowane
                columns['embedding'] = Column(Vector(384))

            model_class = type(class_name, (Base,), {
                '__tablename__': table_name,  # przypisz nazwę tabeli
                **columns,  # dodaj kolumny
                '__table_args__': {'extend_existing': True}  # Dodaj to
            })

            # Dodaj klasę modelu do globalnej przestrzeni nazw
            globals()[class_name] = model_class

        return globals()





