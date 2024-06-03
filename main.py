from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from services.preprocessing.en.EnPreprocessing import EnPreprocessing
from services.index.Index import Index
from services.matching.Matching import Matching
import mysql.connector

app = FastAPI()

class Query(BaseModel):
    query: str
    language: str
preprocess = EnPreprocessing()
index = Index(preprocess)
matching = Matching(preprocess)

#Connecting To Mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="IR"
)
mycursor = mydb.cursor()


@app.get("/")
def read_root():
    return {"Hello": "World"}

#Preprocessing Service

# @app.post("/en_preprocessing")
# async def preprocessing(query: Query):
#     cleaned_text = preprocess.preProcessor(query.text)
#     return {"cleaned text": cleaned_text}

# @app.post("/index")
# async def building_index(docs: Docs):
#     return index.building_index(docs.docs)

@app.post("/search")
async def search(query:Query):
    return matching.search_api(query.query, query.language, mycursor)
