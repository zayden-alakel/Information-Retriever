# IR_Project
 It is an Information Retrieval project that aims to implement various services for text processing, indexing, and querying. The project contain multiple documents and an api to query these documents, So that it returns in the response the most relevant documents to the query according to many metrics.

# Project Structure

##main
  This is the entry point for our project.
##services
  which contains :
  ###Preproccessing
      This is where we use our text proccessing functions. For the Arabic data set we have : non arabic words removal, arabic numbers removal, punctuation removal, stopwords removal, Msa atbrokenizer(which splits the arabic words from the extra letters), text normalizing(normalize_alef maksura,normalize_teh_marbutah,normalize_alef,normalize_dediac), text stemming.
      For the English data set we hava : punctuation removal, text normalizing, stop words removal, text lemmatization.
      We used camel-tools tokenizer for the arabic data set, and NLTK tokenizer for the english data set.
  ###Index
      Here we are building our indexes which is process that identifies and retrieves information system resources relevant to an information need, which can be specified in the form of a search query and also we are building our tfidfVectorizer.
  ###Matching
      Here we are fetching  the results for a specifc query and it is where we also calculate the cosine similarity value.
  ###Evaluation
      Here we ara calculating the evaluation measures such as MAP(mean average precision), Recal, MRR(mean reciprocal rank) and Precision@k.

# Usage


# Languages, Frameworks & Libraries
Front-end Application:


Back-end Application:
- Python
- NLTK
- IR_datasets
  

# Development Team
