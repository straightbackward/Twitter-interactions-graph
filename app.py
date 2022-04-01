from flask import Flask
from flask_cors import CORS
from data import make_graph
from api import all_remaining_slots

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://www.sociogame.net"]}})


@app.route("/user/<screen_name>")
def network_graph(screen_name):
    slots = all_remaining_slots()
    if "reset" in slots:
        return {"error": "Sorry! We reached Twitter limit. Try Later."}
    return make_graph(screen_name)


@app.route("/slots")
def limit():
    return all_remaining_slots()

