from flask import Flask
from flask_cors import CORS
import openai
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from routes.neural.solve_coreferences import solve_coref_blueprint
from routes.neural.solve_not_in_text import solve_not_in_text_blueprint
from routes.symbolic.process_ontology import process_ontology_blueprint
from routes.symbolic.get_ontology_class import get_classes_blueprint
from routes.neural.topics import topics_blueprint
from routes.neural.execute import execute_blueprint
from routes.symbolic.calc_confidence_score import calc_confidence_score_blueprint
from routes.symbolic.process_text import process_text_blueprint
from routes.symbolic.get_sentence import get_sentence_blueprint

load_dotenv()

# load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION = os.environ.get("OPENAI_ORGANIZATION")

# set openai api key and organization

# TODO: The 'openai.organization' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(organization=OPENAI_ORGANIZATION)'
# openai.organization = OPENAI_ORGANIZATION

# create flask app
app = Flask(__name__)
CORS(app, origins="http://localhost:3000", methods=["GET", "POST", "OPTIONS"])

# register blueprints
app.register_blueprint(solve_coref_blueprint)
app.register_blueprint(solve_not_in_text_blueprint)
app.register_blueprint(process_ontology_blueprint)
app.register_blueprint(get_classes_blueprint)
app.register_blueprint(topics_blueprint)
app.register_blueprint(execute_blueprint)
app.register_blueprint(calc_confidence_score_blueprint)
app.register_blueprint(process_text_blueprint)
app.register_blueprint(get_sentence_blueprint)

connection_string = os.getenv("CONNECTION_STRING")
mode = os.getenv("MODE")


@app.route("/")
def hello():
    print("Verifying connection to database:", connection_string, flush=True)
    engine = create_engine(connection_string)

    # verify connection
    with engine.connect() as con:
        rs = con.execute(text("select * from information_schema.schemata"))
        print(rs.fetchone())

    print("Connection established via SQL Alchemy", flush=True)

    return "OK"


# run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
# if mode == "dev":
# else:
#     app.run(host='0.0.0.0', port=80, debug=True, ssl_context=("fullchain.pem", "privkey.pem"))
