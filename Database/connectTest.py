from DatabaseConnect import DatabaseConnect
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import text
import traceback
from Entity.Models import Models

databaseConnect = DatabaseConnect()
sessionDb = databaseConnect.DbConnect()

models = Models()
globals = models.createModels()

try :
    initial_prompts = globals.get('Initial_prompts')
    print(initial_prompts)
    print("\n ******************* \n")
    result = sessionDb.query(initial_prompts).all()

    # sessionDb.query("initial_prompts").all()
    # result = sessionDb.execute(text("SELECT * FROM initial_prompts")).fetchall()
    for row in result:
        print(f"ID: {row.id}, Prompt: {row.model_name}")  # Dostosuj do nazw kolumn

    sessionDb.commit()
except Exception as e:
    error_details = traceback.format_exc()
    print(f"MYSQL ERROR: {error_details}")
    sessionDb.rollback()  # Cofnięcie transakcji
finally:
    sessionDb.close()
