from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from scipy import sparse

class Index:

    default_dir = "C:/Users/Ahmed/Desktop/index_output/"
    def __init__(self, preprocess):
        self.preprocess = preprocess
        #self.output_dir = output_dir

    def savigng_model(self, model):
        with open(self.default_dir+'model_object.pkl', 'wb') as outp:
            pickle.dump(model, outp, pickle.HIGHEST_PROTOCOL)
        return "model saved successfully"
    
    def saving_index(self, index):
        sparse.save_npz(self.default_dir+'index.npz', index)
        return "index saved successfully"
    
    def building_index(self, docs_list: list):
        vectorizer = TfidfVectorizer(tokenizer=self.preprocess.tokenizer, preprocessor=self.preprocess.preProcessor)
        index = vectorizer.fit_transform(docs_list)
        self.savigng_model(vectorizer)
        self.saving_index(index)
        print(vectorizer.get_feature_names_out())
        return "Building Index done, check your model and index in your output directory"
