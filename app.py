from flask import Flask
from flask import jsonify
from data import make_graph
app = Flask(__name__)

@app.route("/<screen_name>")
def network_graph(screen_name):
    return make_graph(screen_name)


