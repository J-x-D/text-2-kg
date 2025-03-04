from flask import Blueprint, request, jsonify
from rdflib import Graph as RDFGraph, Namespace, URIRef, Literal, BNode, RDF, FOAF
from rdflib.namespace import XSD
import json
from fastcoref import spacy_component
import spacy
from spacy.lang.en import English  # updated
import pandas as pd
import uuid
from sqlalchemy import create_engine, text
import os
from utils.get_embedding import get_sbert_embedding

connection_string = os.getenv("CONNECTION_STRING")

process_text_blueprint = Blueprint("process_text", __name__)


@process_text_blueprint.route("/process_text", methods=["POST"])
def process_text():
    try:
        # access the request body
        data = request.get_json()["text"]
        id = str(hash(data))

        nlp = English()
        nlp.add_pipe("sentencizer")
        doc = nlp(data)
        sentences = [sent for sent in doc.sents]
        print("Sentences:", sentences, flush=True)

        # create dataframe with rows for each sentence and columns for the sentence and the uuid
        df = pd.DataFrame(columns=["hash", "sentence", "embedding"])

        # get embedding for each sentence
        for sentence in sentences:
            embedding = get_sbert_embedding(sentence.text).tolist()
            row = {"hash": id, "sentence": sentence.text, "embedding": embedding}
            df.loc[len(df.index)] = row

        # save dataframe via sqlalchemy
        engine = create_engine(connection_string)
        df.to_sql("sentences", con=engine, if_exists="replace")
        print("Saved sentences to database...", flush=True)

        return jsonify({"id": id}), 200
    except Exception as e:
        print("Error while processing text:", str(e), flush=True)
        return jsonify({"error": "Error while processing text"}), 500
