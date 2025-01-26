from Database.DatabaseConnect import DatabaseConnect
from Entity.Models import Models
from datetime import datetime
from sqlalchemy import or_

class FirstPrompts():

    def __init__(self, parametrs=None):
        if parametrs is None:
            parametrs = {}
        self._parametrs = parametrs

    @property
    def parametrs(self):
        return self._parametrs

    @parametrs.setter
    def parametrs(self, new_value):
        self._parametrs = new_value

    def initPrompts(self):

        databaseConnect = DatabaseConnect()
        sessionDb = databaseConnect.DbConnect()
        models = Models()
        globals = models.createModels()

        python_master_filter = ""
        if self._parametrs['python_master'] == True:
            python_master_filter = "python_programer"

        initial_prompts = globals.get('Initial_prompts')
        result = sessionDb.query(initial_prompts).filter(
            or_(
                initial_prompts.prompt_name == 'basic',
                initial_prompts.prompt_name == python_master_filter
            )
        ).all()

        current_datetime = datetime.now()
        prompt = f"Today is {current_datetime}. "
        for row in result:
            prompt += row.prompt+"\n"

        sessionDb.commit()
        sessionDb.close()

        # print( "\033[93m" + prompt + "\033[0m")
        
        return prompt