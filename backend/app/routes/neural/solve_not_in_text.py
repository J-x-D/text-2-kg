import openai
from openai import OpenAI

import os
from flask import Blueprint, Flask, jsonify, render_template, request
from dotenv import load_dotenv
import json

load_dotenv()


response_data = ""

solve_not_in_text_blueprint = Blueprint("solve_not_in_text", __name__)


@solve_not_in_text_blueprint.route("/solve_not_in_text", methods=["POST"])
def get_solve_not_in_text():
    global response_data
    text = request.json.get("text")
    error_key = request.json.get("error_key")
    triple = request.json.get("triple")

    if not text:
        return jsonify({"error": "No input provided"}), 400

    print("\033[94m" + "calling llm to solve that s/o is not in text" + "\033[0m")

    return solve_not_in_text(text, error_key, triple)

def solve_not_in_text(text, error_key, triple):
    template = """
        {
            "subject": {"text":"<some text from the text>", "value": "<the value based on the text (can be a summary)"},
            "predicate": {"text":"<some text from the text>", "value": "<the value based on the text (can be a summary)"},
            "object": {"text":"<some text from the text>", "value": "<the value based on the text (can be a summary)"}
        }
        """
    try:
        prompt = f"""
                In the following triple the {error_key} does not occur in the text. Please provide a {error_key} that occurs in the text and fits to the previous {error_key}. 
                text = {text} 
                triple =  {triple}

                Use the following template to provide the {error_key}:
                {template}

                Exchange the {error_key} with a {error_key} that occurs in the text and means the same.
                Avoid any explanation.
                """
        
        print(prompt, flush=True)

        client = OpenAI(os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            response_format="json",
            temperature=0.0,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        # Its now a dict, no need to worry about json loading so many times
        response_data = completion.model_dump()
        print(response_data, flush=True)
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
    return response_data, 200
