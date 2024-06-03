from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, words;
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk import pos_tag
import string
import re

class EnPreprocessing:

    stopWords = stopwords.words('English') + ["'d", "'ll", "'re", "'s", "'ve", 'could', 'might', 'must', "n't", 'need', 'sha', 'wo', 'would','arent', 'couldnt', 'didnt', 'doesnt', 'dont', 'hadnt', 'hasnt', 'havent', 'isnt', 'mightnt', 'mustnt', 'neednt', 'nt', 'shant', 'shes', 'shouldnt', 'shouldve', 'thatll', 'wasnt', 'werent', 'wont', 'wouldnt', 'youd', 'youll', 'youre', 'youve''arent', 'couldnt', 'didnt', 'doesnt', 'dont', 'hadnt', 'hasnt', 'havent', 'isnt', 'mightnt', 'mustnt', 'neednt', 'nt', 'shant', 'shes', 'shouldnt', 'shouldve', 'thatll', 'wasnt', 'werent', 'wont', 'wouldnt', 'youd', 'youll', 'youre', 'youve']
    words = set(words.words())
    string.punctuation = "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    lemmatizerr = WordNetLemmatizer()

    def get_wordnet_pos(slef, tag_parameter):
        tag = tag_parameter[0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    def tokenizer(self, text):
        return word_tokenize(text)

    def list_to_string(self, list):
        return ' '.join(map(str, list))

    def remove_numbers(self, text):
        return re.sub(r'\d+', '', text)

    def normalization(self, text):
        return text.lower()

    def remove_links(self,text):
        return re.sub(r'\b(?:https?://|www\d{0,3}\.)\S+\b', '', text)

    def stop_words_remove(self, text):
        result = []
        for word in word_tokenize(text):
            if word not in self.stopWords:
                result.append(word)
        return self.list_to_string(result)

    def verb_adj_lemma(self,text):
        words1 = word_tokenize(text)
        text1 = ' '.join([WordNetLemmatizer().lemmatize(word, pos='v') for word in words1])
        words2 = word_tokenize(text1)
        text2 = ' '.join([WordNetLemmatizer().lemmatize(word, pos='a') for word in words2])
        text_pos = pos_tag(word_tokenize(text2)) 
        answer = ' '.join([WordNetLemmatizer().lemmatize(word, pos=self.get_wordnet_pos(tag)) for word, tag in text_pos])
        return answer

    def lemmatizer(self,text):
        text_pos = pos_tag(word_tokenize(text))
        lemmatized = [self.lemmatizerr.lemmatize(word, pos=self.get_wordnet_pos(tag)) for word, tag in text_pos]
        return self.list_to_string(lemmatized)

    def stemmer(self, text):
        words = word_tokenize(text)
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in words]
        return self.list_to_string(stemmed_words)

    def punctuation_remove(self,text):
        return text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

    def remove_meaningless_word(self,text):
        return " ".join(w for w in word_tokenize(text) if w.lower() in words or not w.isalpha())

    def remove_spaces(self,text):
        return " ".join(text.split())
        
    def remove_non_alphanumeric(self,text):
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)

    def remove_short_words(self,text):
        return re.sub(r'\b\w{1,2}\b', '', text)

    @staticmethod
    def preProcessor(self,text):
        text1 = self.normalization(text)
        text2 = self.remove_links(text1)
        text3 = self.remove_numbers(text2)
        text4 = self.punctuation_remove(text3)
        text5 = self.remove_non_alphanumeric(text4)
        text6 = self.remove_spaces(text5)
        text7 = self.verb_adj_lemma(text6)
        text8 = self.stop_words_remove(text7)
        text9 = self.remove_short_words(text8)
        text10 = self.remove_meaningless_word(text9)
        return text10