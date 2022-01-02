from matplotlib import colors, lines
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error, r2_score

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