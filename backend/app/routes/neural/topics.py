import openai
from openai import OpenAI
import os
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import json

load_dotenv()


response_data = ""

topics_blueprint = Blueprint("topics", __name__)


@topics_blueprint.route("/topics", methods=["POST"])
def get_response_data():
    global response_data
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "No input provided"}), 400

    print("\033[94m" + "calling LLM" + "\033[0m")

    template = """
            ["<some topic>", "<some topic>", "<some topic>"]
    """

    try:
        prompt = f"""
                Provide triples, contaning of subjects, predicates, and objects based on the following text. 
                text = {text}  

                Do not transform, summarize or reformulate the text even if it is not grammatically correct any more.
                Every content of a subject, predicate and object should occur exactly the same in the text.
                Do not remove anything from the text not even a single character.
                The triples should be in the following format:
                {template}
                Avoid any explanation.
                """

        client = OpenAI(os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-4",
            response_format="json",
            seed=42,
            temperature=0.5,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        # Its now a dict, no need to worry about json loading so many times
        response_data = completion.model_dump()

    except openai.RateLimitError as e:
        # request limit exceeded or something.
        print(e)
        return jsonify({"error": "".format(e)}), 429
    except json.decoder.JSONDecodeError as jde:
        return jsonify({"Error": "{}".format(jde)}), 500
    except Exception as e:
        # general exception handling
        print(e)
        
    return jsonify({"error": "".format(e)}), 400


    # print in green
    print("\033[92m" + "generated message" + "\033[0m")
    return jsonify(response_data)
