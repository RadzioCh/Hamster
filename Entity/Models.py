from Database.DatabaseConnect import DatabaseConnect
from sqlalchemy import Column, LargeBinary, Integer, ForeignKey
from pgvector.sqlalchemy import Vector

class Models():
    def createModels(self):
        databaseConnect = DatabaseConnect()
        databaseInfo = databaseConnect.DbConnectAndMetadata()

        metadata = databaseInfo["metadata"]
        Base = databaseInfo["Base"]

        # Przechodzenie przez wszystkie tabele w metadanych
        for table_name, table in metadata.tables.items():
            class_name = table_name.capitalize()
            columns = {}

            # Tworzenie kolumn
            for column in table.columns:
                # Specjalne traktowanie kolumny embedding
                if column.name == "embedding":
                    columns[column.name] = Column(Vector(384))
                else:
                    columns[column.name] = column

            # Dodanie kluczy obcych
            for foreign_key in table.foreign_keys:
                fk_column = foreign_key.parent.name
                target_table = foreign_key.column.table.name
                target_column = foreign_key.column.name

                # Zaktualizuj kolumnę o ForeignKey
                columns[fk_column] = Column(
                    Integer, 
                    ForeignKey(f"{target_table}.{target_column}")
                )

            # Tworzenie klasy modelu
            model_class = type(class_name, (Base,), {
                '__tablename__': table_name,
                **columns,
                '__table_args__': {'extend_existing': True}  # Pozwala na nadpisywanie tabel
            })

            # Rejestracja w globalnej przestrzeni nazw
            globals()[class_name] = model_class

        return globals()






