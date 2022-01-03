from matplotlib import colors, lines
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import matplotlib.pyplot as plt

# funcion para el primer análisis
## Regresion lineal

titulosReportes = ['Tendencia de la infección por Covid-19 en un país']

def TendenciaInfeccion(archivo, pais, infecciones, etiquetaPais, predicciones =[]):
    now = datetime.now()
    try :            

        if '.csv' in archivo: # El archivo es un csv
            dataframe = pd.read_csv('./archivos/'+archivo)

        if '.xls' in archivo: #El archivo es un excel
            dataframe = pd.read_excel('./archivos/'+archivo)

        if '.xlsx' in archivo: #El archivo es un excel
            dataframe = pd.read_excel('./archivos/'+archivo)

        ## Filtramos el dataframe para solo tener el pais que se ha indicado        
        dataframe = dataframe[(dataframe.Pais == pais )]

        ## La lista de objetos, es decir las columnas que tienen valores no numericos
        listaObjetos = dataframe.select_dtypes(include = ["object", 'datetime']).columns
        #print(listaObjetos)

        le =LabelEncoder()

        # Feature = caracteristica feat
        for feat in listaObjetos:
            dataframe[feat] = le.fit_transform(dataframe[feat].astype(str))

        if(infecciones==None):
            dataframe_caracteristicas = dataframe.drop([infecciones], axis=1)#.reshape((-1,1))            
        else:
            dataframe_caracteristicas = dataframe.drop([infecciones], axis=1)#.reshape((-1,1))
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
        for prediccion in predicciones:
            valorpredicciones[prediccion] = modelo.predict([[valorPredecir]])
        
        ## Grafica
        generarGrafica(dataframe_caracteristicas['Dia'], dataframe_objetivo, titulosReportes[0], 'Fechas' , 'Muertes')

        return {
            "coeficiente": r2,
            "r2" : r2,
            "rmse" : rmse,
            "mse" : mse,
            "predicciones" : valorpredicciones,
            "timestamp": now.strftime("%d/%m/%Y %H:%M:%S"),
            "code" : 200
        }
        
    except Exception as e: 
        print('ERROR!!!!!!!!!!',str(e))
        return {
            "mensaje" : str(e),
            "code" : 666,
            "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")
        }        



def generarGrafica(X,y, titulo, etiquetaX, etiquetaY):
    X_grid=np.arange(min(X),max(X),0.1)
    X_grid=X_grid.reshape((len(X_grid),1))
    plt.scatter(X,y,color='red')
    plt.plot(X,lin_reg2.predict(poly_reg.fit_transform(X)),color='blue')
    plt.title(titulo)
    plt.xlabel(etiquetaX)
    plt.ylabel(etiquetaY)
    plt.savefig('reporte1.png')    






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