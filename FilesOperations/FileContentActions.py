import sys
import os
# from Models.MistralCall import MistralCall
from transformers import pipeline
import yake
hamster_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(hamster_root)
from sentence_transformers import SentenceTransformer
from Database.DatabaseConnect import DatabaseConnect
from Entity.Models import Models
from datetime import datetime
from sqlalchemy.types import UserDefinedType
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import func
import numpy as np
import psycopg2
from Database.EmbeddingSql import EmbeddingSql
from sqlalchemy.orm import aliased



class FileContentActions():

    def __init__(self):
        # self.mistralCall = MistralCall()
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", revision="main")

    def deleteFileContent(self):
        databaseConnect = DatabaseConnect()
        sessionDb = databaseConnect.DbConnect()
        models = Models()
        model_classes = models.createModels()

        sessionDb.query(model_classes['File_contents']).delete()
        sessionDb.commit()

        sessionDb.query(model_classes['File_keywords']).delete()
        sessionDb.commit()

        sessionDb.query(model_classes['Files']).delete()
        sessionDb.commit()

        

    def insertFileContend(self, fileParametrs, typeInsert):

        fieldPrepare = []
        for filePath, content in fileParametrs.items():
            fileName = os.path.basename(filePath)
            fregments = self.splitTextWithOverlap(content)
            
            # shortcut = self.summarize_text(content)
            keywords = self.extract_keywords(content, "pl", 3, 0.9, 25)

            fieldPrepare.append({
                "file_name": fileName,
                "file_content": fregments['fragments'],
                # "file_embending_content": fregments['embendingFragment'],
                "file_keywords": keywords
            })
        
        databaseConnect = DatabaseConnect()
        sessionDb = databaseConnect.DbConnect()
        models = Models()
        model_classes = models.createModels()
        # print(globals['Files'])
        # sys.exit()

        if typeInsert == "discusion":
            for fileParametrs in fieldPrepare:
                
                new_file = model_classes['Files'](
                    file_name=fileParametrs['file_name'],
                    created_at=datetime.now()  # jeśli masz takie pole; w przeciwnym wypadku usuń ten argument
                )
                sessionDb.add(new_file)
                last_file = sessionDb.query(model_classes['Files']).filter(
                        model_classes['Files'].id == sessionDb.query(func.max(model_classes['Files'].id)).scalar_subquery()
                    ).first()

                new_keywords_list = []
                for keyword, weight in fileParametrs['file_keywords']:
                    new_keywords_list.append(model_classes['File_keywords'](
                        file_id=last_file.id,
                        keyword=keyword,
                        score=float(weight)
                    ))
                sessionDb.add_all(new_keywords_list)

                new_file_content_list = []
                order = 1
                for fragment, embedding in fileParametrs['file_content']:
                    new_file_content_list.append(model_classes['File_contents'](
                        file_id=last_file.id,
                        fragment_order=order,
                        content=fragment,
                        embedding=embedding.tolist()
                    ))
                    order += 1

                sessionDb.add_all(new_file_content_list)
                sessionDb.commit()
            # print(fileParametrs)
        else:
            print('Remember file content')

        
        sessionDb.close()
            
    def splitTextWithOverlap(self, text, max_length=1000, overlap=50):
        fragments = []
        embendingFragment = []
        start = 0
        while start < len(text):
            end = start + max_length
            fragment = text[start:end] # + "\n\n\n ********************************* \n\n\n"
            # embendingFragment.append( self.embendingText(fragment) )
            embedding = self.embendingText(fragment)
            fragments.append([fragment, embedding])
            start += (max_length - overlap)
        return {"fragments": fragments}  # Return the list of fragments
    
    def summarize_text(self, text):
        summary = self.summarizer(text, max_length=200, min_length=150, do_sample=False)
        return summary[0]['summary_text']

    def extract_keywords(self, text, language="pl", max_ngram_size=2, deduplication_threshold=0.9, numOfKeywords=20):
        """
        Wyciąganie słów kluczowych z tekstu.
        Parameters
        ----------
        text : str
            Tekst, z którego wyciągane są słowa kluczowe.
        language : str, optional
            Język tekstu (default: "pl").
        max_ngram_size : int, optional
            Maksymalny rozmiar ngramu (default: 2).
        deduplication_threshold : float, optional
            Progi duplikacji (default: 0.9).
        numOfKeywords : int, optional
            Liczba słów kluczowych do wygenerowania (default: 20).
        
        Returns
        -------
        list
            Lista słów kluczowych, gdzie każdy element jest krotką (słowo, wagowość).
        """
        kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
        keywords = kw_extractor.extract_keywords(text)
        return keywords

    def embendingText(self, text):
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embeddings = model.encode(text)
        return embeddings
    
    def precisionSearch(self):
        '''
        POdejście dla precyzyjnych wyszukiwań, gdy ktoś szuka bardzo konkretnych fragmentów.

        Im większy próg tym ((np. 0.7 → 0.9)) więcej ogólnych wyników dostaniesz.
        Im mniejszy próg (np. 0.3 → 0.5),  tym bardziej podobne wyniki otrzymasz.
        '''
        embeddingSql = EmbeddingSql()
        embedding_vector = embeddingSql.get_embedding_to_text('co to Wartości niematerialne')


        # print(embedding_vector)

        databaseConnect = DatabaseConnect()
        sessionDb = databaseConnect.DbConnect()
        models = Models()
        globals = models.createModels()

        file_contents = globals.get('File_contents')
        result = sessionDb.query(file_contents).filter(
                func.cosine_distance(file_contents.embedding, embedding_vector) < 0.7
        ).all()

        # for row in result:
        #     print('********************************')
        #     print(row.content)

        sessionDb.commit()
        sessionDb.close()

        return result

    def lookForALooseResemblance(self, question, similartStep):
        '''
        Podejście idealne dla luźnych zapytań, gdy użytkownik nie pamięta dokładnych słów, ale chce znaleźć coś zbliżonego.

        Im większy próg (np. 0.7 → 0.9), tym bardziej podobne wyniki otrzymasz.
        Im mniejszy próg (np. 0.3 → 0.5), tym więcej ogólnych wyników dostaniesz.
        '''
        embeddingSql = EmbeddingSql()
        embedding_vector = embeddingSql.get_embedding_to_text(question)

        databaseConnect = DatabaseConnect()
        sessionDb = databaseConnect.DbConnect()
        models = Models()
        globals = models.createModels()

        

        file_contents = globals.get('File_contents')
        files_data = globals.get('Files')

        # print(file_contents.__table__)  # Wyświetla strukturę tabeli
        # print(files_data.__table__)  # Wyświetla strukturę tabeli
        # sys.exit()

        similarity = 1 - func.cosine_distance(file_contents.embedding, embedding_vector)
        result = (
            sessionDb.query(
                file_contents.id,
                files_data.file_name,
                file_contents.content,
                similarity.label("similarity")
            )
            .join(files_data, files_data.id == file_contents.file_id)
            .filter(similarity >= similartStep)
            .order_by(similarity.desc())
            .limit(3)
            .all()
        )

        

        # print(result)
        # for row in result:
        #     print('********************************')
        #     print(row.content[:35])
        #     print(row.similarity)

        sessionDb.commit()
        sessionDb.close()

        return result
    
    def test_lookForALooseResemblance(self,question, similarity_thresholds):
        """
        Test wykonujący zapytanie przy różnych progach podobieństwa i zwracający wyniki.
        
        :param question: Zapytanie, które chcemy wyszukać w bazie
        :param similarity_thresholds: Lista progów podobieństwa do przetestowania (np. [0.9, 0.7, 0.5])
        """
        embeddingSql = EmbeddingSql()
        embedding_vector = embeddingSql.get_embedding_to_text(question)

        databaseConnect = DatabaseConnect()
        sessionDb = databaseConnect.DbConnect()
        models = Models()
        globals = models.createModels()

        file_contents = globals.get('File_contents')

        # Iteracja przez różne progi
        for threshold in similarity_thresholds:
            similarity = 1 - func.cosine_distance(file_contents.embedding, embedding_vector)
            result = sessionDb.query(
                file_contents.id,
                file_contents.content,
                similarity.label("similarity")
            ).filter(similarity >= threshold).order_by(similarity.desc()).limit(3).all()

            print(f"Results for threshold {threshold}:")
            for row in result:
                print('********************************')
                print(f"ID: {row[0]}")
                print(f"Content: {row[1][:30]}")
                print(f"Similarity: {row[2]}")
                print()

        sessionDb.commit()
        sessionDb.close()

    def getContentByFile(self, question, similartStep):
        result = self.lookForALooseResemblance(question, similartStep)

        text = '<contents>'
        
        for row in result:
            text += '<source_file_name>'+row.file_name+'</source_file_name>'
            text += '<content>'+row.content + '</content>'
        text += '</contents>'

        return text