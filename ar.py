import pandas as pd
import re
import pickle
import string
import numpy as np
from scipy import sparse
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, words;
from nltk.tokenize import word_tokenize
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
from nltk.stem.isri import ISRIStemmer
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer
from camel_tools.tokenizers.word import simple_word_tokenize as tokenizer
from camel_tools.utils.normalize import normalize_unicode, normalize_alef_maksura_ar, normalize_teh_marbuta_ar, normalize_alef_ar
from camel_tools.utils.dediac import dediac_ar


stopWords = stopwords.words('English') + ["'d", "'ll", "'re", "'s", "'ve", 'could', 'might', 'must', "n't", 'need', 'sha', 'wo', 'would','arent', 'couldnt', 'didnt', 'doesnt', 'dont', 'hadnt', 'hasnt', 'havent', 'isnt', 'mightnt', 'mustnt', 'neednt', 'nt', 'shant', 'shes', 'shouldnt', 'shouldve', 'thatll', 'wasnt', 'werent', 'wont', 'wouldnt', 'youd', 'youll', 'youre', 'youve''arent', 'couldnt', 'didnt', 'doesnt', 'dont', 'hadnt', 'hasnt', 'havent', 'isnt', 'mightnt', 'mustnt', 'neednt', 'nt', 'shant', 'shes', 'shouldnt', 'shouldve', 'thatll', 'wasnt', 'werent', 'wont', 'wouldnt', 'youd', 'youll', 'youre', 'youve']
additonal_words = ['cigarettes', 'vaping', 'vape', 'privatize', 'palestinian', 'israeli']
words = set(words.words())
words.update(additonal_words)
string.punctuation = "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
#"!#$%&'()*+,-./:;<=>?@[\]^_`{|}~≤…•¾–—‘’“”≡"
lemmatizerr = WordNetLemmatizer()

def get_wordnet_pos(tag_parameter):
    tag = tag_parameter[0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def tokenizer(text):
    return word_tokenize(text)

def list_to_string(list):
    return ' '.join(map(str, list))

def remove_numbers(text):
    return re.sub(r'\d+', '', text)

def normalization(text):
    return text.lower()

def remove_links(text):
    return re.sub(r'\b(?:https?://|www\d{0,3}\.)\S+\b', '', text)

def stop_words_remove(text):
    result = []
    for word in word_tokenize(text):
        if word not in stopWords:
            result.append(word)
    return list_to_string(result)

def verb_adj_lemma(text):
    words1 = word_tokenize(text)
    text1 = ' '.join([WordNetLemmatizer().lemmatize(word, pos='v') for word in words1])
    words2 = word_tokenize(text1)
    text2 = ' '.join([WordNetLemmatizer().lemmatize(word, pos='a') for word in words2])
    text_pos = pos_tag(word_tokenize(text2)) 
    answer = ' '.join([WordNetLemmatizer().lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag in text_pos])
    return answer

def lemmatizer(text):
    text_pos = pos_tag(word_tokenize(text))
    lemmatized = [lemmatizerr.lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag in text_pos]
    return list_to_string(lemmatized)

def stemmer(text):
    words = word_tokenize(text)
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]
    return list_to_string(stemmed_words)

def punctuation_remove(text):
    return text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

def remove_meaningless_word(text):
    return " ".join(w for w in word_tokenize(text) if w.lower() in words or not w.isalpha())

def remove_spaces(text):
    return " ".join(text.split())
    
def remove_non_alphanumeric(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def remove_short_words(text):
    return re.sub(r'\b\w{1,2}\b', '', text)

def preProcessor(text):
    text1 = normalization(text)
    text2 = remove_links(text1)
    text3 = remove_numbers(text2)
    text4 = punctuation_remove(text3)
    text5 = remove_non_alphanumeric(text4)
    text6 = remove_spaces(text5)
    text7 = verb_adj_lemma(text6)
    text8 = stop_words_remove(text7)
    text9 = remove_short_words(text8)
    text10 = remove_meaningless_word(text9)
    return text10
