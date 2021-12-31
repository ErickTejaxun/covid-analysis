from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask import send_file, current_app as app
import json
from json import JSONEncoder
import os

EntornoGlobal = None
ArbolAnterior = None
app = Flask(__name__)



def obtenerParametros(option):
    if option == '1': ## Tendencia de la infección por Covid-19 en un país
        parametros = [
                {'id': 'etiquetaPais','nombre': 'Etiqueta País', 'valorActual': "contry"},
                {'id': 'nombrePais', 'nombre': 'Nombre del País', 'valorActual': "Guatemala"},
                {'id': 'etiquetaInfecciones', 'nombre': 'Etiqueta infección por día', 'valorActual': "cases_per_day"}
        ]    
        return parametros
    if option == '2': ## Predicción de Infertados en un País
        parametros = [
                {'nombre': 'Etiqueta País', 'valorActual': "contry"},
                {'nombre': 'Nombre del País', 'valorActual': "Guatemala"},
                {'nombre': 'Etiqueta casos', 'valorActual': "cases"}
        ]    
        return parametros        


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

@app.route("/getParametros", methods=["POST", "GET"])
def getParametros():
    option = '1'
    if request.method == "POST":
        option = request.form["option"]
    return jsonify(obtenerParametros(option))     

@app.route("/descargar" , methods=["POST"])
def descargar():      
    return redirect("/static/ast.gv.pdf")

if __name__ == "__main__":    
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)#para que se actualice al detectar cambios



