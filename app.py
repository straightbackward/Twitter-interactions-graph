from flask import Flask
from flask import jsonify
from data import make_graph
from api import limit_status
app = Flask(__name__)

@app.route("/user/<screen_name>")
def network_graph(screen_name):
    return make_graph(screen_name)


@app.route("/slots")
def limit():
    return limit_status()

