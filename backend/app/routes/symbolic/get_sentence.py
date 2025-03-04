from sqlalchemy import create_engine
from flask import Blueprint, request, jsonify
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from utils.get_embedding import get_sbert_embedding
from sentence_transformers import util
from thefuzz import process
import re


get_sentence_blueprint = Blueprint(" get_sentence", __name__)

# load environment variables
connection_string = os.getenv("CONNECTION_STRING")


@get_sentence_blueprint.route("/get_sentence", methods=["POST"])
def get_sentence():
    id = request.json["id"]
    search = request.json["query"]
    sentence = get_sentence_item(id, search)
    return jsonify({"sentence": sentence}), 200


def get_sentence_item(id, search):
    table_name = "sentences"

    # load dataframe with classes from database where the ontology_url is in the list of ontologies
    engine = create_engine(connection_string)

    # Construct the SQL query with dynamic placeholders
    query = f"SELECT * FROM {table_name} WHERE hash = '{id}'"

    df = pd.read_sql_query(query, engine)
    print("Loaded dataframe:", df, flush=True)

    splitted_search = re.sub(
        "([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", search)
    ).split()
    search = " ".join(splitted_search)
    print("Search:", search, flush=True)

    # create embedding of query
    query_embedding = get_sbert_embedding(search)

    # access the column with the embeddings and convert it to a list
    embeddings = df["embedding"].tolist()

    # parse every embedding in the list of embeddings to a numpy array
    embeddings = [
        np.fromstring(embedding[1:-1], dtype=np.float32, sep=",")
        for embedding in embeddings
    ]

    # combine the list of embeddings to a numpy array
    embeddings = np.array(embeddings)

    # calculate the cosine similarity between the query embedding and all the embeddings in the dataframe
    hits = util.semantic_search(
        query_embedding, embeddings, score_function=util.dot_score, top_k=10
    )[0]

    indexes_scores = [
        {"index": hit["corpus_id"], "score": hit["score"]} for hit in hits
    ]
    print("Indexes scores:", indexes_scores, flush=True)

    # # create a list with dicts of the class and the score
    # top_10 = []
    # for index_score in indexes_scores:
    #     top_10.append({'sentence': df['sentence'][index_score['index']], 'score': index_score['score'], 'index': index_score['index']})

    # print("Top 10 before:", top_10, flush=True)

    # fuzzy_matches = process.extract(search, df['sentence'].tolist(), limit=10)

    # # parse fuzzy matches to a dict with the class and the score
    # fuzzy_matches = [{'sentence': fuzzy_match[0], 'score': fuzzy_match[1]} for fuzzy_match in fuzzy_matches]

    # for fuzzy_match in fuzzy_matches:
    #     match_found = False
    #     for top_10_item in top_10:
    #         if fuzzy_match['sentence'] == top_10_item['sentence']:
    #             fuzzy_match['score'] = (fuzzy_match['score'] + top_10_item['score']) / 2
    #             match_found = True
    #             break  # exit the inner loop once a match is found

    #     if not match_found:
    #         top_10.append(fuzzy_match)

    # # append fuzzy matches to top_10 list
    # top_10.extend(fuzzy_matches)

    # sort the list based on the score
    # top_10 = sorted(indexes_scores, key=lambda k: k['score'], reverse=True)

    # take top result
    top_result = indexes_scores[0]
    print("Top result:", top_result, flush=True)

    # get the sentence with the highest score
    sentence = df["sentence"][top_result["index"]]
    print("Sentence:", sentence, flush=True)
    return sentence
