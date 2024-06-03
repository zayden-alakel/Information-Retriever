import pandas as pd
#loading en_corpus
en_corpus = pd.read_csv('C:/Users/Ahmed/Desktop/data/en_corpus.csv')

#loading en_quereies
en_queries = pd.read_json("C:/Users/Ahmed/Desktop/data/en_queries.jsonl", lines=True)

#loading en_qrels
en_qrels = pd.read_csv("C:/Users/Ahmed/Desktop/data/en_qrels.tsv", sep="\t")

#loading ar_corpus
ar_corpus = pd.read_csv('C:/Users/Ahmed/Desktop/data/ar_corpus.csv')

#loading ar_quereies
ar_queries = pd.read_csv("C:/Users/Ahmed/Desktop/data/ar_queries.csv", delimiter="\t")

# #loading ar_qrels file
ar_qrels = pd.read_csv("C:/Users/Ahmed/Desktop/data/ar_qrels.csv")