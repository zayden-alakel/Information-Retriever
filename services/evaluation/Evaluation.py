import data
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Evaluation:

    def similarity_queries(self, vectorizer, index):
        test = pd.DataFrame(0, index=["cosine"], columns=data.corpus["_id"], dtype=np.float64)
        for index, row in data.en_queries.iterrows():
            query_vector = vectorizer.transform([row['text']])
            result = cosine_similarity(index, query_vector).flatten()
            test.loc['cosine'] = result
            sorted_test = test.sort_values(by="cosine", axis=1, ascending=False)
            sorted_test.to_csv(f"C:/Users/Ahmed/Desktop/cosine_similarity/{index}.csv", index=False)
        print("done cosine similarity")

    def revelance_matrix(self):
        map_matrix = np.full((49, 10), False)
        for index, row in data.ar_queries.iterrows():
            cos_similarity = pd.read_csv(f"C:/Users/Ahmed/Desktop/cosine_similarity/{index}.csv")
            first_ten_values = cos_similarity.iloc[0, :10]
            for k, (doc, cos) in enumerate(first_ten_values.items()):
                for i, value in data.en_qrels.iterrows():
                    if(index == value["query-id"]-1):
                        if(doc == value["corpus-id"]):
                            map_matrix[index][k] = True
                    else: continue
        np.savetxt('C:/Users/Ahmed/Desktop/map.txt', map_matrix, fmt='%d')
        return map_matrix

    def claculate_map(self):
        actual = self.revelance_matrix()
        Q = len(actual)
        predicted = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        k = 10
        ap = []
        ap_num = 0    
        for x in range(k):        
            act_set = set(actual[self.q])        
            pred_set = set(predicted[:x+1])
            precision_at_k = len(act_set & pred_set) / (x+1)
            if predicted[x] in actual[self.q]:
                rel_k = 1        
            else:
                rel_k = 0    
        ap.append(self.ap_q)
        return sum(ap) / Q