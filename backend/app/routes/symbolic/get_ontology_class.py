
from sqlalchemy import create_engine
from flask import Blueprint, request
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from utils.get_embedding import get_sbert_embedding
from sentence_transformers import  util
from thefuzz import process

get_classes_blueprint = Blueprint(
    'get_classes', __name__)

# load environment variables
connection_string = os.getenv('CONNECTION_STRING')


@get_classes_blueprint.route("/get_classes", methods=['POST'])
def get_classes():
    ontologies = request.json['ontologies']
    search = request.json['query']
    return get_ontology_item(ontologies, search, "class")

@get_classes_blueprint.route("/get_properties", methods=['POST'])
def get_properties():
    ontologies = request.json['ontologies']
    search = request.json['query']
    return get_ontology_item(ontologies, search, "property")


def get_ontology_item(ontologies, search, identifier):
    table_name = "ontology_classes"

    if(identifier == "property"):
        table_name = "ontology_properties"

    # load dataframe with classes from database where the ontology_url is in the list of ontologies
    engine = create_engine(connection_string)
    
    # Generate parameter placeholders based on the number of elements in the ontologies list
    placeholders = ', '.join(['%s'] * len(ontologies))

    # Construct the SQL query with dynamic placeholders
    query = f"SELECT * FROM {table_name} WHERE ontology_url IN ({placeholders})"
    params = tuple(ontologies)  # Convert the list to a tuple for the parameter

    df = pd.read_sql_query(query, engine, params=params)

    # create embedding of query
    query_embedding = get_sbert_embedding(search)

    # access the column with the embeddings and convert it to a list
    embeddings = df['embedding'].tolist()

    # parse every embedding in the list of embeddings to a numpy array
    embeddings = [np.fromstring(embedding[1:-1], dtype=np.float32, sep=',') for embedding in embeddings]

    # combine the list of embeddings to a numpy array
    embeddings = np.array(embeddings)

    # calculate the cosine similarity between the query embedding and all the embeddings in the dataframe
    hits = util.semantic_search(query_embedding, embeddings, score_function=util.dot_score, top_k=10)[0]

    indexes_scores = [{'index': hit['corpus_id'], 'score': hit['score']} for hit in hits]

    # create a list with dicts of the class and the score
    top_10 = []
    for index_score in indexes_scores:
        top_10.append({identifier: df.iloc[index_score['index']][identifier], 'score': round(index_score['score'] * 100), 'ontology_url': df.iloc[index_score['index']]['ontology_url']})


    fuzzy_matches = process.extract(search, df[identifier].tolist(), limit=10)

    # parse fuzzy matches to a dict with the class and the score
    fuzzy_matches = [{identifier: match[0], 'score': match[1], 'ontology_url': df.iloc[df[df[identifier] == match[0]].index[0]]['ontology_url']} for match in fuzzy_matches]

    # if element is already in the top_10 list, update the score with the average of the two scores and add the element to the top_10 list and remove it from the fuzzy_matches list
    for fuzzy_match in fuzzy_matches:
        for top_10_item in top_10:
            if fuzzy_match[identifier] == top_10_item[identifier]:
                top_10_item['score'] = (fuzzy_match['score'] + top_10_item['score']) / 2
                fuzzy_matches.remove(fuzzy_match)

    # append fuzzy matches to top_10 list
    top_10.extend(fuzzy_matches)

    # sort the list based on the score
    top_10 = sorted(top_10, key=lambda k: k['score'], reverse=True)
                    
    # return only the class column as a list
    return top_10