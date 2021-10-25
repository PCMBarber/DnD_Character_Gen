from flask import render_template, redirect, url_for, Response, request, jsonify
import random
from application import app
import json

@app.route('/', methods=['POST'])
def back_end():
    skills=[request.get_json()["strength"],request.get_json()["dexterity"],request.get_json()["constitution"],request.get_json()["intelligence"],request.get_json()["wisdom"],request.get_json()["charisma"]]
    
    dice={"1":request.get_json()["1"],"2":request.get_json()["2"],
    "3":request.get_json()["3"],"4":request.get_json()["4"],
    "5":request.get_json()["5"],"6":request.get_json()["6"]}

    sort=[]

    for skill in skills:
        for key in dice:
            if key == skill:
                sort.append(dice[key])
    strength=sort[0]
    dexterity=sort[1]
    constitution=sort[2]
    intelligence=sort[3]
    wisdom=sort[4]
    charisma=sort[5]
    return jsonify({"char_name":request.get_json()["char_name"],"race":request.get_json()["race"],"char_class":request.get_json()["char_class"],
        "strength":strength, "dexterity":dexterity,"constitution":constitution,
        "intelligence":intelligence,"wisdom":wisdom,"charisma":charisma,"feats":request.get_json()["feats"]
        })