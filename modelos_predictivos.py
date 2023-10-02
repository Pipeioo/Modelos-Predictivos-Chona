# -*- coding: utf-8 -*-
"""Modelos Predictivos

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X_tdGeKqq9o-4yVr707wSDNnrPeRFeez
"""

!pip install sklearn

import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score
from sklearn.impute import SimpleImputer

# Cargar el dataset
df = pd.read_csv('dataset_olympics.csv')

df['Medal'].fillna( 0, inplace=True)
df['Height'].fillna( 0, inplace=True)
df['Weight'].fillna( 0, inplace=True)
df['Age'].fillna( 0, inplace=True)
df['Year'].fillna( 0, inplace=True)

df['Medal'].replace(['Gold', 'Silver', 'Bronze'], 1, inplace=True)

df



# Visualizar la distribución de los datos
sns.pairplot(df)
# Visualizar la matriz de correlación
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')

X = df[['Year', 'Weight', 'Age']]  # Características
y_num = df['Medal']  # Atributo a predecir

# Contar cuántos valores en y_num son iguales a '0'
num_zeros = (y_num == '0').sum()

if num_zeros > 0:
    # Dividir los datos en entrenamiento y prueba solo si hay valores '0' en y_num
    X_train, X_test, y_train_num, y_test_num = train_test_split(X, y_num, test_size=0.2, random_state=42)

    # Crear y entrenar el modelo de regresión lineal
    regression_model = LinearRegression()
    regression_model.fit(X_train, y_train_num)

    # Evaluar el modelo
    regression_score = regression_model.score(X_test, y_test_num)
    print("Cantidad de medallas", regression_score)

y_bin = df['Medal']  # Atributo categórico binario a predecir

# Convertir el atributo categórico a numérico usando LabelEncoder
label_encoder = LabelEncoder()
y_bin_encoded = label_encoder.fit_transform(y_bin)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train_bin, y_test_bin = train_test_split(X, y_bin_encoded, test_size=0.2, random_state=42)

# Crear y entrenar el modelo de árbol de decisión
tree_model = DecisionTreeClassifier(random_state=42)
tree_model.fit(X_train, y_train_bin)

# Evaluar el modelo
y_pred_bin = tree_model.predict(X_test)
accuracy = accuracy_score(y_test_bin, y_pred_bin)
conf_matrix = confusion_matrix(y_test_bin, y_pred_bin)
classification_rep = classification_report(y_test_bin, y_pred_bin)
print("Accuracy para árbol de decisión:", accuracy)
print("Matriz de confusión:\n", conf_matrix)
print("Reporte de clasificación:\n", classification_rep)

# Validación cruzada para regresión lineal
regression_cv_scores = cross_val_score(regression_model, X, y_num, cv=5)

# Validación cruzada para árbol de decisión
tree_cv_scores = cross_val_score(tree_model, X, y_bin_encoded, cv=5)

print("Resultados de validación cruzada para regresión lineal:", regression_cv_scores)
print("Resultados de validación cruzada para árbol de decisión:", tree_cv_scores)

"""Conclusion:
Los graficos ayudan a entender mejor tu dataset y poder obvservar la disposicion de los datos.

Tambien permiten ver todo de manera mas ordenada y gráfica, y asi sacar distintas conclusiones como por ejemplo: el peso promedio estimado de los deportistas olimpicos.
"""