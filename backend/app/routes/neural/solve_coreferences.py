from flask import Blueprint, request, jsonify
from rdflib import Graph as RDFGraph, Namespace, URIRef, Literal, BNode, RDF, FOAF
from rdflib.namespace import XSD
import json
from fastcoref import spacy_component
import spacy

solve_coref_blueprint = Blueprint("solve_coref", __name__)


@solve_coref_blueprint.route("/solve_coreferences", methods=["POST"])
def solve_coreferences():
    print("Calling solve_coreferences", flush=True)
    try:
        # access the request body
        data = request.get_json()["text"]
        print("Solving coreferences for text:", data, flush=True)

        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("fastcoref")

        doc = nlp(data, component_cfg={"fastcoref": {"resolve_text": True}})
        response = doc._.resolved_text
        return jsonify({"response": response}), 200
    except Exception as e:
        print("Error while solving coreferences:", str(e), flush=True)
        return jsonify({"error": "Error while solving coreferences"}), 500
