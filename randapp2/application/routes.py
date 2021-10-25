from flask import render_template, redirect, url_for, Response, request, jsonify
import random
from application import app
import json

@app.route('/')
@app.route('/background', methods=['GET','POST'])
def background():
    backgrounds=['Acolyte','Charlatan','Criminal / Spy','Entertainer','Folk Hero','Gladiator','Guild Artisan / Guild Merchant','Knight','Noble','Pirate','Sage','Soldier','Urchin']
    choice=random.choice(backgrounds)

    return jsonify({"Background":choice})