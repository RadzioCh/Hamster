from Database.DatabaseConnect import DatabaseConnect
from Entity.Models import Models
from datetime import datetime

class FirstPrompts():

    def initPrompts(self):

        databaseConnect = DatabaseConnect()
        sessionDb = databaseConnect.DbConnect()
        models = Models()
        globals = models.createModels()

        initial_prompts = globals.get('Initial_prompts')
        result = sessionDb.query(initial_prompts).filter(initial_prompts.prompt_name == "basic").all()

        current_datetime = datetime.now()
        prompt = f"Today is {current_datetime}. "
        for row in result:
            prompt += row.prompt+"\n"

        sessionDb.commit()
        sessionDb.close()
        
        return prompt