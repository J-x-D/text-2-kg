import openai
from openai import OpenAI
from rdflib import Graph
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import json

load_dotenv()


response_data = ""

execute_blueprint = Blueprint("execute", __name__)


@execute_blueprint.route("/execute", methods=["POST"])
def get_response_data():
    global response_data
    prompt = request.json.get("prompt", "")
    serialize = request.json.get("serialize", False)
    if not prompt:
        return jsonify({"error": "No input provided"}), 400

    print("\033[94m" + "calling LLM" + "\033[0m")
    print("\033[94m" + "prompt: " + prompt + "\033[0m")

    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        # Its now a dict, no need to worry about json loading so many times
        response_data = completion.choices[0].message.content
        print("\033[94m" + "response: " + response_data + "\033[0m")

        if serialize:
            jsonld = serialize_response(response_data), 200
            return jsonld

    except Exception as e:
        # general exception handling
        error_prompt = """
                    An error occured while executing your response.
                    You will be penalized.
                    ### Instruction ###
                    Please try again and fix the error described below.
                    You MUST provide a valid TURTLE response based on the instructions provided.

                    ### Error ###
                    {}
                    """.format(e)
        print(error_prompt)
        client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },{
                    "role": "system",
                    "content": response_data,
                },
                {
                    "role": "user",
                    "content": error_prompt
                }
            ],
        )
        response_data = completion.choices[0].message.content
        print("\033[94m" + "new response: " + response_data + "\033[0m")
        if serialize:
            jsonld = serialize_response(response_data), 200
            return jsonld
        return jsonify(response_data)
    except:
        return jsonify({"error": str(e)}), 500
    
    return jsonify(response_data), 200


def serialize_response(response):
    g = Graph()
    g.parse(data=response, format="turtle")
    jsonld = g.serialize(format="json-ld")
    print("\033[94m" + "serialized: " + jsonld + "\033[0m")
    return jsonld

