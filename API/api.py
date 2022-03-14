# Librairies
# from crypt import methods
# from crypt import methods
from ast import dump
from unittest import result
from bson.json_util import dumps
import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify, send_file, safe_join, make_response
import json
import os
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import requests
from bson.objectid import ObjectId
from pprint import pprint
from matplotlib.font_manager import json_dump
from pymongo import MongoClient
from flask_pymongo import PyMongo
import streamlit as st




cwd = os.getcwd()

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'secretkey'

app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
mongo = PyMongo(app)
# CONNEXION A LA BASE DE DONNEES
# Client
client = MongoClient('localhost', 27017)
# Base de données
dba = client["api"]
# # Collections
chemises = mongo.db.chemises
# chemises = dba["chemises"]
print('connexion success')

# mongo = PyMongo(app, uri="mongodb://localhost:27017/databaseOne")

# LES ENDPOINTS


@app.route('/')
def index():
    return 'Api with chemises of Zalando site scrappé!'

# route pour aficher nos données


@app.route("/chemises", methods=['GET', 'POST'])
def all_chemises():
    our_chemises = list(chemises.find({}, {'_id': 0}))
    #resp = dumps(chemises)
    
    if request.method == 'GET':
        print(our_chemises[0]['nom_chemise'])
        return jsonify({'error_code': 200, 'result': our_chemises}), 200
    else:
        return jsonify({"error_code": 404, "error_message": "Mauavises methode pour afficher nos données"}), 404


@app.route("/chems", methods=['GET', 'POST'])
def all():
    our_chemises = chemises.find({}, {'_id': 0})
    resp = dumps(our_chemises)
    dictionnaire_chems = {}
    # stocker les colonnes dans des variables pour mieux les reutiliser dans streamlit
    # 'nom_chemise': 0, 'description': 0, 'old-price': 0, 'newpricecol': 0
    name_chems = chemises.find({}, {'_id': 0, 'description': 0, 'old-price': 0, 'newpricecol': 0})
    desc_chems = chemises.find({}, {'_id': 0, 'nom_chemise': 0, 'old-price': 0, 'newpricecol': 0})
    old_chems_price = chemises.find({}, {'_id': 0, 'nom_chemise': 0, 'description': 0, 'newpricecol': 0})
    new_chems_price = chemises.find({}, {'_id': 0, 'nom_chemise': 0, 'description': 0, 'old-price': 0 })
    
    # Tableau pour entrer les valeurs dedans
    # dictionnaire_chems = {""}
    
    
    
    if request.method == 'GET':
        return jsonify(resp)
        # return jsonify({'result': resp})
    else:
        return jsonify({"error_code": 404, "error_message": "Mauavises methode pour afficher nos données"}), 404

@app.route("/ ", methods=['GET', 'POST'])
def all_chemises_objectID():
    our_chemises = chemises.find()
    resp = dumps(our_chemises)
    if request.method == 'GET':
        return jsonify({'error_code': 200, 'result': resp}), 200
    else:
        return jsonify({"error_code": 404, "error_message": "Mauavises methode pour afficher nos données"}), 404


@app.route("/chemises_id/<id>", methods=['GET', 'POST'])
def one_chemises():
    find_id = chemises.find_one({'_id':ObjectId(id)})
    # chemises.find_one({'_id':ObjectId(id)})
    if request.method == 'GET':
        return jsonify({'error_code': 200, 'result': find_id}), 200
    else:
        return jsonify({"error_code": 404, "error_message": "Mauavises methode pour afficher nos données"}), 404



@app.route("/chemises_by_name/<name>", methods=['GET', 'POST'])
def chemise_by_name(name):
    one_chemise = list(chemises.find({"nom_chemise": name}, {'_id': 0}))
    # result = list(chemises.find_one({"nom_chemise" : {$regex : name}}, {'_id':0}));
    if name == str:
        if request.method == 'GET':
            if one_chemise == True:
                return jsonify({'error_code': 200, 'result': one_chemise}), 200
                # return jsonify({'error_code': 200, 'result': result}), 200
        else:
            return jsonify({'error_code': 404, 'error_message': 'bad method u use'}), 404
    else:
        return jsonify({"error_code": '404', 'error_message 1': 'Verifiez que vous avez rentré une chaine de caractere'}), 404


# @app.route("/chemises_by_id/<int:id>", methods=['GET', 'POST'])
# def chemise_by_id(id):
#     if request.method == 'GET':
#         # qui contient le texte rentré par le user
#         result = list(chemises.find({}, {'_id': 0}))[int(id)]
#         return jsonify({'error_code': 200, 'result': result}), 200
#     else:
#         return jsonify({"error_codee": '404', 'error_message 1': 'mauvaise requete', 'error_message 2': 'id doit être un int', 'error_message 3': 'Out of range'}), 404


# Route pour créer une données
@app.route("/inserts/one", methods=['POST'])
def addone():
    _json = request.json  # (force=True)
    # _json = json.dumps(_json)
    _nom_chemise = _json['nom_chemise']
    _description = _json['description']
    _old_price = _json['old-price']
    _newpricecol = _json['newpricecol']

    # convert dict to json and insert the result

    if _nom_chemise and _description and _old_price and _newpricecol and request.method == 'POST':
        # _jsonObject = json.dumps(_json)
        print(type(chemises))
        chemises.insert_one({"nom_chemise": _nom_chemise, "description": _description, "old-price": _old_price, "newpricecol": _newpricecol})
        # db_insert_one = chemises.insert(_json)
        return jsonify({'error_code': '200', 'error_message': 'vos données ont été ajouté à la fin de la collection', "inserted by you": _json}), 200
    else:
        return jsonify({'error_code': '404', 'error_message': "vos données n'ont pas été ajoutées verifier que c'est un dictionnaire ou que ce sont les bonnes clés, ou que c'est un seul document que vous avez rentré"}), 404

# @app.route("insert/many", methods=['POST', 'PUT'])
# def addone():
#     if request.method == 'POST':
#         data = request.get_json()
#         db_insert_one = chemises.insert_many(data)
#         return 'vos données ont été ajouté à la fin de la collection'
#     else:
#         return "vos données n'ont pas été ajoutées verifier que c'est un dictionnaire ou que ce sont les bonnes clés", 404


# Route pour update une données
@app.route("/update/<id>", methods=['PUT'])
def updateone(id):
    _json = request.json
    id_toupdate = id
    _nom_chemise = _json['nom_chemise']
    _description = _json['description']
    _old_price = _json['old-price']
    _newpricecol= _json['newpricecol']

    if _nom_chemise and _description and _old_price and _newpricecol and request.method == 'PUT':
        chemises.update_one({'_id': ObjectId(id_toupdate['$oid']) if '$oid' in id_toupdate else ObjectId(id_toupdate)}, {'$set': {'nom_chemise': _nom_chemise, 'description': _description, 'old-price': _old_price, 'newpricecol':_newpricecol}})
        return jsonify({'error_code':200, 'message':'Update successfuly'})
    else:
        return jsonify({'error_code': 404, 'message':'not update'}), 404

    # dataup = request.get_json()
    # if request.method == 'PUT':
    #     try:
    #         update_value = chemises.update_one({"_id": ObjectId(id_toupdate)})
    #         return jsonify({"error_code": "200", "error_message": "Il a été delete successfuly", "id": f"{id_toupdate}"}), 200
    #     except ValueError:
    #         return jsonify({"error_code": "404", "error_message": "Cannot delete la chemise"}), 404
    # db_update = chemises.update_one(
    #     {'_id':ObjectId(id)}
    #     {
    #        $set:
    # )
    # return
# $$
# @app.route("/update/<id>", methods=['PUT'])
# def updateone_objectid():
#     _json = request.json
#     id_toupdate = _json['id']
#     _nom_chemise = _json['nom_chemise']
#     _description = _json['description']
#     _old_price = _json['old-price']
#     _newpricecol= _json['newpricecol']

#     if _nom_chemise and _description and _old_price and _newpricecol and request.method == 'PUT':
#         chemises.update_one({'_id': ObjectId(id_toupdate['$oid']) if '$oid' in id_toupdate else ObjectId(id_toupdate)}, {'$set': {'nom_chemise': _nom_chemise, 'description': _description, 'old-price': _old_price, 'newpricecol':_newpricecol}})
#         return jsonify({'error_code':200, 'message':'Update successfuly'})
#     else:
#         return jsonify({'error_code': 404, 'message':'not update'}), 404
    
    
# ---------------------
# # Route pour supprimer une donnée
# @app.route("/deletes/<id_todelete>", methods=['DELETE'])
# def deleteone(id_todelete):
#     try:
#         delete_value = chemises.delete_one({"_id": ObjectId(int(id_todelete))})
#         return jsonify({"error_code": "200", "error_message": "Il a été delete successfuly", "id": f"{id}"}), 200
#     except ValueError:
#         return jsonify({"error_code": "404", "error_message": "Cannot delete la chemise"}), 404
    

@app.route('/delete_id/<id>', methods=['DELETE'])
def delete_chemise_id(id):
    chemises.delete_one({'_id': ObjectId(id)})
    return jsonify({"error_code": "200", "error_message": "delete ssuccessfuly"}), 200
    
# @app.route('/delete_id/<name>', methods=['DELETE'])
# def delete_chemise_name(id):
#     deleteone_by_id = chemises.delete_one({'_id': ObjectId((id))})
#     if id :
#         return jsonify({"error_code": "200", "error_message": "Cannot delete la chemise"}), 200

# MAIN ...


# VIA HTML 

@app.route("/home_html")
def documentation():
    json_documents = list(chemises.find({}, {'_id': 0}))
    #resp = dumps(chemises)
    if request.method == 'GET':
        return jsonify({'error_code': 200, 'result': json_documents}), 200
    else:
        return jsonify({"error_code": 404, "error_message": "Mauavises methode pour afficher nos données"}), 404



@app.route("/create_html")
def create():
    if request.method == "POST":     
        
        req = request.form
        
        missing = list()
        # Prendre les input de l'utilisateur
        nom_chemise = request.form["nom_chemise"]
        description = request.form["description"]
        old_price = request.form["old-price"]
        newpricecol = request.form["newpricecol"]
        
        # manquant
        
        for k, v in req.items():
            if v == "":
                missing.append(k)
                
        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("/form_create.html", feedback=feedback)
        
        if 'nom_chemise' and 'description' and 'old-price' and 'newpricecol' :
            # chemises_add_one = chemises.insert({"nom_chemise": nom_chemise, "description": description, "old-price": old_price, "newpricecol": newpricecol})
            chemises.insert({"nom_chemise": nom_chemise, "description": description, "old-price": old_price, "newpricecol": newpricecol})
            # new_book = book.find_one({'_id': books_id })
            # output = {'name' : new_book['name'], 'title' : new_book['title'], 'category' : new_book['category']}
            
            flash("Insertion reussie")
                    
        print(req)
        
        
        return redirect(request.url)
    return render_template('/form_create.html')


@app.route("/update_html")
def update_html():
    if request.method == "POST":
        req = request.form
        
        missing = list()
        # Prendre les input de l'utilisateur
        nom_chemise = request.form["nom_chemise"]
        description = request.form["description"]
        old_price = request.form["old-price"]
        newpricecol = request.form["newpricecol"]
        
        # manquant
        
        for k, v in req.items():
            if v == "":
                missing.append(k)
                
        if missing:
            feedback = f"Missing fields for {', '.join(missing)}" 
            return render_template("/form_update.html", feedback=feedback)
        
        print(req)
        return redirect(request.url)
    return render_template('/form_update.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
