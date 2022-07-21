import os
from flask import Flask
from flask_cors import CORS
from data import make_graph
from api import all_remaining_slots
from flask import request
from db import put_sale, get_sale

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["https://www.sociogame.net"]}})


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


#gumroad:  ImmutableMultiDict([('seller_id', 'Zz29KlYoVw2jxJw9AG1RHg=='), ('product_id', '3YRQ3Zwr3ZItSABwvswDRg=='), ('product_name', 'Sociogram'), ('permalink', 'skip'), ('product_permalink', 'https://sociogame.gumroad.com/l/skip'), ('short_product_id', 'tazwu'), ('email', 'ali98mim@gmail.com'), ('price', '0'), ('gumroad_fee', '0'), ('currency', 'usd'), ('quantity', '1'), ('discover_fee_charged', 'false'), ('can_contact', 'true'), ('referrer', 'direct'), ('card[bin]', ''), ('card[expiry_month]', ''), ('card[expiry_year]', ''), ('card[type]', ''), ('card[visual]', ''), ('order_number', '487183159'), ('sale_id', '40W9K7DL8I8vLU0U5a9rmA=='), ('sale_timestamp', '2022-07-20T14:30:20Z'), ('purchaser_id', '8728212710766'), ('offer_code', 'vaslolkhetab'), ('test', 'true'), ('Username you want its graph', 'miishoow'), ('custom_fields[Username you want its graph]', 'miishoow'), ('license_key', '9517ECD3-B4C64921-8598D99B-40C008A6'), ('ip_country', 'France'), ('is_gift_receiver_purchase', 'false'), ('refunded', 'false'), ('disputed', 'false'), ('dispute_won', 'false')])
