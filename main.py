from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask import send_file, current_app as app
import json
from json import JSONEncoder
import os

EntornoGlobal = None
ArbolAnterior = None
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/reports", methods=["POST", "GET"])
def reports():
    if request.method == "POST":
        inpt = request.form["valor"]
    else:
        return render_template('reports.html')

@app.route("/descargar" , methods=["POST"])
def descargar():      
    return redirect("/static/ast.gv.pdf")

if __name__ == "__main__":    
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)#para que se actualice al detectar cambios