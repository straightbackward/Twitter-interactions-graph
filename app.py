from flask import Flask
from flask_cors import CORS
from data import make_graph
from api import all_remaining_slots

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://www.sociogame.net"]}})


@app.route("/user/<screen_name>")
def network_graph(screen_name):
    all_remaining_slots()
    return make_graph(screen_name)


@app.route("/slots")
def limit():
    return str(all_remaining_slots())

