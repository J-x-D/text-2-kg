import openai
from openai import OpenAI
from rdflib import Graph
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import json
import os
import anthropic

load_dotenv()

response_data = ""
execute_blueprint = Blueprint("execute", __name__)


def call_openai(prompt, model):
    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content


def call_deepseek(prompt, model):
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
    )
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content


def call_claude(prompt, model):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=20000,
        temperature=1,
        messages=[
            {"role": "user", "content": [{"type": "text", "text": prompt}]},
        ],
    )
    return message.content


def get_model_response(prompt, model):
    if model.startswith("gpt-"):
        return call_openai(prompt, model)
    elif "claude" in model:
        return call_claude(prompt, model)
    else:
        return call_deepseek(prompt, model)


@execute_blueprint.route("/execute", methods=["POST"])
def get_response_data():
    global response_data
    prompt = request.json.get("prompt", "")
    serialize = request.json.get("serialize", False)
    model = request.json.get("model", "gpt-4")  # TODO: change default

    if not prompt:
        return jsonify({"error": "No input provided"}), 400

    print("\033[94mcalling LLM\033[0m")
    print(f"\033[94mprompt: {prompt}\033[0m")

    try:
        response_data = get_model_response(prompt, model)
        print(f"\033[94mresponse: {response_data}\033[0m")

        if serialize:
            jsonld = serialize_response(response_data), 200
            return jsonld

    except Exception as e:
        error_prompt = f"""
            An error occurred while executing your response.
            You will be penalized.
            ### Instruction ###
            Please try again and fix the error described below.
            You MUST provide a valid TURTLE response based on the instructions provided.
            
            ### Error ###
            {e}
        """
        print(error_prompt)
        response_data = get_model_response(error_prompt, "gpt-4")
        print(f"\033[94mnew response: {response_data}\033[0m")

        if serialize:
            jsonld = serialize_response(response_data), 200
            return jsonld
        return jsonify(response_data)

    return jsonify(response_data), 200


def serialize_response(response):
    g = Graph()
    g.parse(data=response, format="turtle")
    jsonld = g.serialize(format="json-ld")
    print(f"\033[94mserialized: {jsonld}\033[0m")
    return jsonld
