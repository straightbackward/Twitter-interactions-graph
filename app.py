import os
from flask import Flask
from flask_cors import CORS
from data import make_graph
from api import all_remaining_slots
from flask import request
from db import put_sale, get_sale

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}})


@app.route("/user/<screen_name>")
def network_graph(screen_name):
    slots = all_remaining_slots()
    if "reset" in slots:
        return {"error": "Sorry! We reached Twitter limit. Try Later."}
    return make_graph(screen_name)


@app.route("/slots")
def limit():
    return all_remaining_slots()


ping_url_key = os.getenv('PING_URL_KEY')

@app.route(f"/ping{ping_url_key}", methods=['POST'])
def purchase():
    data = request.form
    screen_name = data['Username you want its graph']
    sale_id = data['sale_id']
    timestamp = data['sale_timestamp']
    put_sale(sale_id, screen_name, timestamp)
    print(screen_name)
    return data

@app.route("/premium/<sale_id>")
def get_graph(sale_id):
    sale = get_sale(sale_id)
    print(sale)
    if 'Item' in sale:
        screen_name = sale['Item']['screen_name']
        all_remaining_slots(True)
        return make_graph(screen_name)
    else:
        return {"error" : "The purchase was unsuccessful. If you have made the payment, contact ali98mim@gmail.com."}