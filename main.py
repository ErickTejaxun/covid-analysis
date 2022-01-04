import os
from flask import Flask, flash, url_for, redirect, url_for, render_template, request, jsonify
from flask import send_file, send_from_directory, current_app as app
import json
from json import JSONEncoder
from werkzeug.utils import secure_filename
import pandas as pd
from analisis import *
#import analisis

UPLOAD_FOLDER = './archivos/'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def obtenerListaArchivos():
    lista= os.listdir(os.path.join(app.config['UPLOAD_FOLDER']))
    return lista


def obtenerParametros(option):
    if option == '1': ## Tendencia de la infección por Covid-19 en un país
        parametros = [
                {'id': 'etiquetaPais','nombre': 'Etiqueta País', 'valorActual': "Pais"},
                {'id': 'grados', 'nombre': 'Grados', 'valorActual': "6"},
                {'id': 'nombrePais', 'nombre': 'Nombre del País', 'valorActual': "Guatemala"},
                {'id': 'etiquetaInfecciones', 'nombre': 'Etiqueta infección por día', 'valorActual': "Infectados"},
                {'id': 'feature', 'nombre': 'Feature (X)', 'valorActual': "Dia"}                
        ]    
        return parametros
    if option == '2': ## Predicción de Infertados en un País
        parametros = [
                {'nombre': 'Etiqueta País', 'valorActual': "contry"},
                {'nombre': 'Nombre del País', 'valorActual': "Guatemala"},
                {'nombre': 'Etiqueta casos', 'valorActual': "cases"}
        ]    
        return parametros        


def obtenerEncabezados(file):    
    try:
        if '.csv' in file: # El archivo es un csv
            df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'])+file)
            encabezados = df.columns.values.tolist()        
            #return encabezados.to_json(orient="records") 
            return {
                "encabezados": encabezados,
                "codigo": 100,
                "mensaje": "OK"
            }

        if '.xlsx' in file: #El archivo es un excel
            df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'])+file)
            encabezados = df.columns.values.tolist()
            #return encabezados.to_json(orient="records") 
            return {
                "encabezados": encabezados,
                "codigo": 100,
                "mensaje": "OK"
            }

        if '.xlsx' in file: #El archivo es un excel
            df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'])+file)
            encabezados = df.columns.values.tolist()
            #return encabezados.to_json(orient="records") 
            return {
                "encabezados": encabezados,
                "codigo": 100,
                "mensaje": "OK"
            }
    except Exception as e: 
        return {
            "mensaje": str(e),
            "codigo" : 666
        }

## Endpoints 

@app.route("/")
def home():
    return render_template('index.html', listaArchivos=obtenerListaArchivos())

@app.route("/menu")
def menu():
    return render_template("menu.html", listaArchivos=obtenerListaArchivos())

@app.route("/obtenerPDF/<archivo>", methods=["GET"])
def reports(archivo):
    if request.method == "GET":
        workingdir = os.path.abspath(os.getcwd())
        filepath = workingdir + '/pdfs/'
        return send_from_directory(filepath, archivo)        
        

@app.route("/getParametros", methods=["POST", "GET"])
def getParametros():
    option = '1'
    if request.method == "POST":
        option = request.form["option"]
    return jsonify(obtenerParametros(option))     

@app.route("/cargarArchivo", methods=["POST"])
def cargarArchivoEntrada():
    if request.method == "POST":
        if 'file' not in request.files:            
            return jsonify({"codigo": 100, "mensaje": "No se ha encontadro el archivo."})
        file = request.files['file']
        if file.filename == '':
            return jsonify({"codigo": 100, "mensaje": "No se ha seleccionado el archivo."})
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))        
        return jsonify({"codigo": 200, "mensaje": "Archivo " + file.filename +" almacenado y cargado correctamente.", "archivos" : obtenerListaArchivos(), "archivo":file.filename})


@app.route("/getCampos", methods=["POST"])
def cargarCampos():
    if request.method == "POST":
        nombreArchivo = request.form["archivo"]
        return jsonify(obtenerEncabezados(nombreArchivo))


@app.route("/analisis", methods=["POST"])
def analisis():
    if request.method == "POST":
        codigoAnalisis = request.form["tipoAnalisis"]
        archivoAnalisis = request.form["archivoAnalisis"]
        tipoAnalisis = request.form["tipoAnalisis"]    
        tipoRegresion = request.form["tipoRegresion"]    
        if(codigoAnalisis == '1'):
            pais = request.form["nombrePais"]
            feature = request.form["feature"]
            infecciones = request.form["etiquetaInfecciones"]
            etiquetaPais = request.form["etiquetaPais"]
            #predicciones = str(request.form.getlist("valoresPredecidos")).split(",")
            predicciones = request.form.getlist("valoresPredecidos")
            predicciones = predicciones[0]
            #(archivo, pais, infecciones, etiquetaPais, predicciones)
            if (tipoRegresion == '1' ):
                resultados = TendenciaInfeccionLineal(archivoAnalisis, pais, infecciones, etiquetaPais, feature, predicciones)
                return jsonify(resultados)
            if (tipoRegresion == '2' or tipoRegresion == '0'):
                grados = int(request.form["grados"])
                resultados = TendenciaInfeccionRegresionPolinomial(archivoAnalisis, pais, infecciones, etiquetaPais, feature, predicciones, grados)
                return jsonify(resultados)
            #archivo, pais, infecciones, etiquetaPais, predicciones =[]
    return jsonify({"codigo":400})

@app.route("/descargar" , methods=["POST"])
def descargar():      
    return redirect("/static/ast.gv.pdf")

if __name__ == "__main__":    
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)#para que se actualice al detectar cambios



