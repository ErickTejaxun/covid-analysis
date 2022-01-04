from matplotlib import colors, lines
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
from Generadorpdf import *
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image


# funcion para el primer análisis
## Regresion lineal

titulosReportes = ['Tendencia de la infección por Covid-19 en un país']

def TendenciaInfeccionLineal(archivo, pais, infecciones, etiquetaPais, feature, predicciones):
    now = datetime.now()
    try :            

        if '.csv' in archivo: # El archivo es un csv
            dataframe = pd.read_csv('./archivos/'+archivo)

        if '.xls' in archivo: #El archivo es un excel
            dataframe = pd.read_excel('./archivos/'+archivo)

        if '.xlsx' in archivo: #El archivo es un excel
            dataframe = pd.read_excel('./archivos/'+archivo)


        #dataframe = dataframe.fillna(lambda x: x.median())
        ## Filtramos el dataframe para solo tener el pais que se ha indicado    
        #dataframe = dataframe.loc[dataframe[etiquetaPais] == pais]    
        dataframe = dataframe[dataframe[etiquetaPais] == pais]
        #dataframe = dataframe[(dataframe.Pais == pais )]

        #dataframe['tmp'] = dataframe[infecciones].cumsum()        
        #dataframe = dataframe.fillna(lambda x: x.median())
        ## La lista de objetos, es decir las columnas que tienen valores no numericos
        
        #listaObjetos = dataframe.select_dtypes(include = ["object", 'datetime']).columns
        listaObjetos = dataframe.select_dtypes(include = ["object", 'datetime'], exclude=['number']).columns
        #print(listaObjetos)

        le =LabelEncoder()

        # Feature = caracteristica feat
        for feat in listaObjetos:
            dataframe[feat] = le.fit_transform(dataframe[feat].astype(str))
        

        #dataframe_caracteristicas = dataframe.drop([infecciones], axis=1)#.reshape((-1,1))
        dataframe_caracteristicas = dataframe[feature].values.reshape(-1,1)
        dataframe_objetivo = dataframe[infecciones]


        
        #dataframe_objetivo = dataframe_objetivo['tmp']

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
            #"img" : generarGrafica(modelo, dataframe_caracteristicas, dataframe_objetivo, prediccion_entrenamiento, titulosReportes[0] , ecuacion, 'Fechas' , 'Infectados','reporte1.png'),
            "nombrePdf":nombrePDF
        }   
    except Exception as e: 
        print('ERROR!!!!!!!!!!',str(e))
        return {
            "mensaje" : str(e).replace("\"", "-"),
            "code" : 666,
            "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")
        }

def TendenciaInfeccionRegresionPolinomial(archivo, pais, infecciones, etiquetaPais, feature, predicciones, grados):
    now = datetime.now()
    try :            

        if '.csv' in archivo: # El archivo es un csv
            dataframe = pd.read_csv('./archivos/'+archivo)

        if '.xls' in archivo: #El archivo es un excel
            dataframe = pd.read_excel('./archivos/'+archivo)

        if '.xlsx' in archivo: #El archivo es un excel
            dataframe = pd.read_excel('./archivos/'+archivo)
   

        dataframe = dataframe[dataframe[etiquetaPais] == pais]
        dataframe.fillna(-99999, inplace=True)
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
        
        modelo = PolynomialFeatures(degree=grados, include_bias=False)
        X_poly = modelo.fit_transform(dataframe_caracteristicas)
        modelo.fit(X_poly, dataframe_objetivo)
        lin_reg2=LinearRegression()
        lin_reg2.fit(X_poly,dataframe_objetivo)
                
        nombrePDF = now.strftime("%d%m%Y%H%M%S") + '.pdf'
        nombrePNG = now.strftime("%d%m%Y%H%M%S") + '.png'
        generarPDF(nombrePDF,'Tendencia de la infección por Covid-19 en un país', 'Regresión Polinomial')
        prediccion_entrenamiento = lin_reg2.predict(X_poly)
        mse = mean_squared_error(dataframe_objetivo,prediccion_entrenamiento)
        rmse = np.sqrt(mse)
        r2 = r2_score(dataframe_objetivo,prediccion_entrenamiento)
        #coeficiente_ = lin_reg2.score(dataframe_caracteristicas, dataframe_objetivo)
        #model_intercept = modelo.intercept_ #b0
        #model_pendiente = modelo.coef_ #b1        
        #ecuacion = "Y(x) = "+str(model_pendiente) + "X + (" +str(model_intercept)+')'
        ecuacion ="Y(x) = "

        return {"coeficiente": r2, "r2" : r2, "rmse" : rmse, "mse" : mse, "predicciones" : [], "timestamp": now.strftime("%d/%m/%Y %H:%M:%S"),
            "code" : 200,
            "img" : generarGrafica(modelo, dataframe_caracteristicas, dataframe_objetivo, prediccion_entrenamiento, titulosReportes[0],  ecuacion, 'Fechas' , 'Infectados',nombrePNG),
            #"img" : generarGrafica(modelo, dataframe_caracteristicas, dataframe_objetivo, prediccion_entrenamiento, titulosReportes[0] , ecuacion, 'Fechas' , 'Infectados','reporte1.png'),
            "nombrePdf":nombrePDF
        }   
    except Exception as e: 
        print('ERROR!!!!!!!!!!',str(e))
        return {
            "mensaje" : str(e).replace("\"", "-"),
            "code" : 666,
            "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")
        }



def TendenciaInfeccionPoli(archivo, pais, infecciones, etiquetaPais, feature, predicciones):
    now = datetime.now()
    try :            

        if '.csv' in archivo: # El archivo es un csv
            dataframe = pd.read_csv('./archivos/'+archivo)

        if '.xls' in archivo: #El archivo es un excel
            dataframe = pd.read_excel('./archivos/'+archivo)

        if '.xlsx' in archivo: #El archivo es un excel
            dataframe = pd.read_excel('./archivos/'+archivo)

        #dataframe = dataframe.fillna(lambda x: x.median())
        ## Filtramos el dataframe para solo tener el pais que se ha indicado    
        #dataframe.loc[dataframe[etiquetaPais] == pais]    
        dataframe = dataframe[dataframe[etiquetaPais] == pais]
        #dataframe = dataframe[(dataframe.Pais == pais )]


        dataframe = dataframe.fillna(lambda x: x.median())

        ## La lista de objetos, es decir las columnas que tienen valores no numericos
        listaObjetos = dataframe.select_dtypes(include = ["object", 'datetime'], exclude=['number']).columns
        #print(listaObjetos)

        le =LabelEncoder()

        # Feature = caracteristica feat
        #for feat in listaObjetos:
        #    dataframe[feat] = le.fit_transform(dataframe[feat].astype(str))


        dataframe[infecciones] = dataframe[infecciones].fillna(0)
        
        #dataframe[infecciones] = pd.to_numeric(dataframe[infecciones], errors='coerce')        

        dataframe_caracteristicas = dataframe.drop([infecciones], axis=1)#.reshape((-1,1))
        #dataframe_caracteristicas = dataframe[feature].values.reshape(-1,1)
        dataframe_objetivo = dataframe[infecciones]



        #print('Informacion dataframe tratado')
        #print(dataframe.info())  
        #print(dataframe)      

        
        #print('Shape caracteristicas: ',dataframe_caracteristicas.shape)
        #print(dataframe_caracteristicas)
        #print('Shape objetivo/target', dataframe_objetivo.shape)
        #print(dataframe_objetivo)
        
        
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
        nombrePDF = now.strftime("%d%m%Y%H%M%S") + '.pdf'
        nombrePNG = now.strftime("%d%m%Y%H%M%S") + '.png'        
        generarPDF(nombrePDF,'Tendencia de la infección por Covid-19 en un país RL', 'Regresión Lineal', img)
        return { "coeficiente": r2,"r2" : r2,"rmse" : rmse,"mse" : mse,"predicciones" : valorpredicciones,"timestamp": now.strftime("%d/%m/%Y %H:%M:%S"),"code" : 200,            
            "img" : generarGrafica(modelo, dataframe_caracteristicas[feature], dataframe_objetivo, prediccion_entrenamiento, titulosReportes[0], "", 'Fechas' , 'Infectados',nombrePNG),
            "nombrePdf" : nombrePDF
        }
        
    except Exception as e: 
        print('ERROR!!!!!!!!!!',str(e))
        return {
            "mensaje" : str(e).replace("\"", "-"),
            "code" : 666,
            "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")
        }        




def generarGrafica(modelo, X, y, y_predict, titulo, etiqueta,  etiquetaX, etiquetaY, nombreImagen):
    import os
    import io
    dir = './imagenes/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    X_grid=np.arange(min(X),max(X),0.1)
    X_grid=X_grid.reshape((len(X_grid),1))
    plt.scatter(X,y,label=etiqueta, color='red')
    #plt.plot(X,modelo.predict(poly_reg.fit_transform(X)),color='blue')
    plt.plot(X,y_predict,label=etiqueta,color='blue')
    plt.title(titulo)
    plt.xlabel(etiquetaX)
    plt.ylabel(etiquetaY)
    plt.savefig('./imagenes/'+nombreImagen) 
    plt.close()


    from base64 import encodebytes
    scriptDir = os.path.dirname(__file__)    
    #pil_img = Image.open(os.path.join(scriptDir,'./imagenes/'+nombreImagen) , mode='r') 
    pil_img = Image.open(os.path.join(scriptDir,'./imagenes/'+nombreImagen) , mode='r') 
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') 
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
    return encoded_img      






'''
dataframe = pd.read_csv("./data/pred.csv")

dt_features = np.array([1,2,3,4,5,6,7,8,9,10]).reshape((-1,1))
dt_target = dataframe['A']



modelo = LinearRegression().fit(dt_features,dt_target )

prediccion_entrenamiento = modelo.predict(dt_features)
mse = mean_squared_error(y_true = dt_target, y_pred = prediccion_entrenamiento)
# La raíz cuadrada del MSE es el RMSE
rmse = np.sqrt(mse)
print('Error Cuadrático Medio (MSE) = ' + str(mse))
print('Raíz del Error Cuadrático Medio (RMSE) = ' + str(rmse))

valorPredecir = 30
predicted = modelo.predict([[valorPredecir]])
print('Prediccion ' ,valorPredecir, ': ',predicted)
print('Coeficiente R² ', modelo.score(dt_features,dt_target))
print('slope: (pendiente)', modelo.coef_)
print('coef:', modelo.coef_)



Y_NEW = modelo.predict(dt_features)
rmse = mean_squared_error(dt_target, Y_NEW)
r2 = r2_score(dt_target,Y_NEW)

print('RMSE: ', rmse)
print('R2: ', r2)
'''