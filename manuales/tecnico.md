# Data analysis Covid-19
## Organización de lenguajes y compiladores 2
## Manual de técnico 

El siguiente manual tiene como objetivo indicar de forma técnica el desarrollo de esta aplicación. 

## Aplicación
La aplicación web Data Analysis Covid 19 es una aplicación que permite obtener análisis de datos históricos sobre el COVID 19.
Esta aplicación web monolítica está escrita en lenguaje de programación Python 3.9 y utilizando el framework web Flask. 

## Requisitos técnicos
Para la ejecución local de esta aplicación se solicitan los siguientes requisitos. 
- 1. Sistema Operativo GNU/Linux x86, Sistema Operativo Windows 7 o superior. 
- 2. Python 3.9.7 o superior. 
- 3. PIP 21.3.1 o superior. 

## Librerías
Se requieren las siguientes librerías. 
```bash
Flask==1.1.2
gunicorn
numpy
scipy
joblib
pandas
matplotlib
scikit-learn
openpyxl
fpdf2
```

## Implementación 
La arquitectura de la aplicación es monólitica, por lo cual esta misma aplicación se encarga de la interfaz web y también el proceso de análisis en background. 

## Archivos 
```
.
├── analisis.py
├── archivos
├── core
├── Generadorpdf.py
├── imagenes
├── main.py
├── manuales
├── pdfs
├── Procfile
├── __pycache__
├── README.md
├── requirements.txt
├── static
└── templates
```

- pdfs : Carpeta donde se almacenan temporalmente los archivos PDF. 
- imagenes : Carpeta donde se almacenan temporalmente los archivos PNG. 
- main.py : Script inicial de la aplicación. 
- templates: Templates para la vista del frontend. 
- analisis.py : Script para análisis de datos. 
- Generadorpdf.py : Script para la generación de archivos pdf. 
- Procfile : Archivo de configuración para ejecución en Heroku. 

### Endpoints
- /analisis  
- /getCampos 
- /cargarArchivo 
- /getParametros 
- /obtenerPDF/archivo 


### Análisis de datos. 
Para el análisis de datos se han utilizado los siguientes modelos: 
- 1. Regresión Lineal
- 2. Regresión polinomial
- 3. Regresión Naive Baye 

### Implementación Regresión lineal.:

```python 
def TendenciaInfeccionLineal(archivo, pais, infecciones, etiquetaPais, feature, predicciones):
    now = datetime.now()
    try :            

        if '.csv' in archivo: # El archivo es un csv
            dataframe = pd.read_csv('./archivos/'+archivo)

        if '.xls' in archivo: #El archivo es un excel
            dataframe = pd.read_excel('./archivos/'+archivo)

        if '.xlsx' in archivo: #El archivo es un excel
            dataframe = pd.read_excel('./archivos/'+archivo)
   
        dataframe = dataframe[dataframe[etiquetaPais] == pais]
        listaObjetos = dataframe.select_dtypes(include = ["object", 'datetime'], exclude=['number']).columns

        le =LabelEncoder()

        for feat in listaObjetos:
            dataframe[feat] = le.fit_transform(dataframe[feat].astype(str))

        dataframe_caracteristicas = dataframe[feature].values.reshape(-1,1)
        dataframe_objetivo = dataframe[infecciones]


        
        print('Informacion dataframe tratado')
        print(dataframe.info())  
        print(dataframe)
        print('Shape caracteristicas: ',dataframe_caracteristicas.shape)
        print(dataframe_caracteristicas)
        print('Shape objetivo/target', dataframe_objetivo.shape)
        print(dataframe_objetivo)
        
        
        modelo = LinearRegression().fit(dataframe_caracteristicas, dataframe_objetivo)
        
        prediccion_entrenamiento = modelo.predict(dataframe_caracteristicas)
        
        mse = mean_squared_error(y_true = dataframe_objetivo, y_pred = prediccion_entrenamiento)
        rmse = np.sqrt(mse)
        r2 = r2_score(dataframe_objetivo, prediccion_entrenamiento)
        coeficiente_ = modelo.score(dataframe_caracteristicas, dataframe_objetivo)
        
        valorpredicciones = {}
        if(isinstance(predicciones, str)):
            predicciones = predicciones.split(",")            
        #for prediccion in predicciones:
        #    valorpredicciones[str(prediccion)] = modelo.predict([[200]])
        
                
        model_intercept = modelo.intercept_ #b0
        model_pendiente = modelo.coef_ #b1

        ecuacion = "Y(x) = "+str(model_pendiente) + "X + (" +str(model_intercept)+')'
        nombrePDF = now.strftime("%d%m%Y%H%M%S") + '.pdf'
        nombrePNG = now.strftime("%d%m%Y%H%M%S") + '.png'
        generarPDF(nombrePDF,'Tendencia de la infección por Covid-19 en un país', 'Regresión Lineal')
        return {"coeficiente": r2, "r2" : r2, "rmse" : rmse, "mse" : mse, "predicciones" : valorpredicciones, "timestamp": now.strftime("%d/%m/%Y %H:%M:%S"),
            "code" : 200,
            "img" : generarGrafica(modelo, dataframe_caracteristicas, dataframe_objetivo, prediccion_entrenamiento, titulosReportes[0],  ecuacion, 'Fechas' , 'Infectados',nombrePNG),
            "nombrePdf":nombrePDF
        }   
    except Exception as e: 
        print('ERROR!!!!!!!!!!',str(e))
        return {
            "mensaje" : str(e).replace("\"", "-"),
            "code" : 666,
            "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")
        }  
```


- [Enlace aplicación live](https://covid19-analysis-etejaxun.herokuapp.com/)
- [Repositorio](https://github.com/ErickTejaxun/covid-analysis)



## Autor
- Erick Tejaxun
- 201213050
- erickteja@gmail.com
