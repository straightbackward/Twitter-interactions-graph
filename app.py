from flask import Flask
from flask import jsonify
from data import make_graph
from api import free_slots
app = Flask(__name__)

@app.route("/user/<screen_name>")
def network_graph(screen_name):
    return make_graph(screen_name)


@app.route("/slots")
def limit():
    return free_slots()

