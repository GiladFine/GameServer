from flask import Flask
from flask import request
from flask import jsonify

app =Flask("flask_server")

app_ip_to_player = dict()

game = None

@app.route("/get_button_names", methods=["GET"])
def get_button_names():
    response = game.get_button_names()
    return jsonify(response)


@app.route("/is_need_to_update_hand", methods=["GET"])
def get_button_names():
    response = game.is_need_to_update_hand(app_ip_to_player[request.remote_addr])
    return jsonify(response)


@app.route("/button1_pressed", methods=["POST"])
def post_button1_pressed():
    response = game.button1_handler(app_ip_to_player[request.remote_addr])
    return jsonify(response)


@app.route("/button2_pressed", methods=["POST"])
def post_button2_pressed():
    response = game.button2_handler(app_ip_to_player[request.remote_addr])
    return jsonify(response)


@app.route("/button3_pressed", methods=["POST"])
def post_button3_pressed():
    response = game.button3_handler(app_ip_to_player[request.remote_addr])
    return jsonify(response)


@app.route("/button4_pressed", methods=["POST"])
def post_button4_pressed():
    response = game.button4_handler(app_ip_to_player[request.remote_addr])
    return jsonify(response)


def run_server():
    if not game:
        print "Error at starting Flask : not game object"
    elif not app_ip_to_player:
        print "Error at starting Flask : app_ip to player object dictionary is empty"
    else:
        app.run(host="0.0.0.0", port=int("80"))
