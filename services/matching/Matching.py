import pickle
import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from services.preprocessing.en.EnPreprocessing import EnPreprocessing
import data
import ar

class Matching:

    min_en_cos = 0.6
    min_ar_cos = 0.3
    en_sql = "SELECT content FROM corpus WHERE doc_id = %s"
    ar_sql = "SELECT content FROM ar_corpus WHERE doc_id = %s"

    def __init__(self, preprocess: EnPreprocessing):
        self.preprocess = preprocess
        ar.preProcessor

    def load_model(self, path):
        ar.preProcessor
        with open(path, 'rb') as inp:
            return pickle.load(inp)
    
    def load_index(self, path):
        return sparse.load_npz(path)

    # def get_most_en_relevant(self, query, frame):
    #     vectorizer = self.load_model('C:/Users/Ahmed/Desktop/ir_output_last/en_model.pkl')
    #     index = self.load_index('C:/Users/Ahmed/Desktop/ir_output_last/en_index.npz')

    #     query_vector = vectorizer.transform([query])
    #     result = cosine_similarity(index, query_vector).flatten()
    #     frame.loc['cosine'] = result
    #     frame.sort_values(by="cosine", axis=1, ascending=False ,inplace=True)
    #     ans = frame.iloc[0, :30]
    #     return ans
    
    # def get_most_ar_relevant(self, query, frame):
    #     vectorizer = self.load_model('C:/Users/Ahmed/Desktop/ir_output_last/ar_model.pkl')
    #     index = self.load_index('C:/Users/Ahmed/Desktop/ir_output_last/ar_index.npz')

    #     query_vector = vectorizer.transform([query])
    #     result = cosine_similarity(index, query_vector).flatten()
    #     frame.loc['cosine'] = result
    #     frame.sort_values(by="cosine", axis=1, ascending=False ,inplace=True)
    #     ans = frame.iloc[0, :30]
    #     return ans    

    # def retreive_en_docs(self, relevant, cursor, en_sql):
    #     result=[]
    #     for key, value in relevant.items():
    #         if(value < self.min_en_cos):
    #             break
    #         adr = (key, )
    #         cursor.execute(en_sql, adr)
    #         myresult = cursor.fetchall()
    #         result.append(myresult)
    #     return result
    
    # def retreive_ar_docs(self, relevant, cursor, ar_sql):
    #     result=[]
    #     for key, value in relevant.items():
    #         if(value < self.min_ar_cos):
    #             break
    #         adr = (key, )
    #         cursor.execute(ar_sql, adr)
    #         myresult = cursor.fetchall()
    #         result.append(myresult)
    #     return result

    # def ar_query_api(self, query, cursor, ar_sql):
    #     frame = pd.DataFrame(0, index=["cosine"], columns=data.ar_corpus["doc_id"], dtype=np.float64)
    #     most_relevant = self.get_most_relevant(query, frame)
    #     return self.retreive_ar_docs(most_relevant, cursor, ar_sql)
    
    # def en_query_api(self, query, cursor, en_sql):
    #     frame = pd.DataFrame(0, index=["cosine"], columns=data.en_corpus["_id"], dtype=np.float64)
    #     most_relevant = self.get_most_relevant(query, frame)
    #     return self.retreive_en_docs(most_relevant, cursor, en_sql)

    def search_api(self, query, language, mycursor):
        api_result = []
        if(language == 'ENGLISH'):
            test = pd.DataFrame(0, index=["cosine"], columns=data.en_corpus["_id"], dtype=np.float64)
            vectorizer = self.load_model('C:/Users/Ahmed/Desktop/ir_output_last/en_model.pkl')
            index = self.load_index('C:/Users/Ahmed/Desktop/ir_output_last/en_index.npz')
        else:
            test = pd.DataFrame(0, index=["cosine"], columns=data.ar_corpus["doc_id"], dtype=np.float64)
            vectorizer = self.load_model('C:/Users/Ahmed/Desktop/ir_output_last/ar_model.pkl')
            index = self.load_index('C:/Users/Ahmed/Desktop/ir_output_last/ar_index.npz')

        query_vector = vectorizer.transform([query])
        result = cosine_similarity(index, query_vector).flatten()
        test.loc['cosine'] = result
        test.sort_values(by="cosine", axis=1, ascending=False ,inplace=True)
        ans = test.iloc[0, :30]

        if(language == 'ENGLISH'):
            for key, value in ans.items():
                if(value < self.min_en_cos):
                    break
            adr = (key, )
            mycursor.execute(self.en_sql, adr)
            myresult = mycursor.fetchall()
            api_result.append(myresult)
        else:
            for key, value in ans.items():
                if(value < self.min_ar_cos):
                    break
            adr = (key, )
            mycursor.execute(self.ar_sql, adr)
            myresult = mycursor.fetchall()
            api_result.append(myresult)
        return api_result    