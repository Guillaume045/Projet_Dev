import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error

def Prevision(csv_path, lag=3):
    data = pd.read_csv(csv_path)
    X = data.iloc[:, -1].to_frame()

    for i in range(1, lag + 1):
        X[f'lag_{i}'] = X['Temperature'].shift(i)

    # Supprimer les valeurs manquantes / Séparer les données en ensembles d'entraînement et de test
    X.dropna(inplace=True)
    train_size = int(len(X) * 0.8)
    train, test = X[0:train_size], X[train_size:]

    # Diviser les caractéristiques (X) et la variable cible (y) pour l'entraînement et le test
    train_X, train_y = train.drop(columns=['Temperature']), train['Temperature']
    test_X, test_y = test.drop(columns=['Temperature']), test['Temperature']

    # Créer et entraîner le modèle AR
    model = AutoReg(train_y, lags=lag)
    model_fit = model.fit()
    predictions = model_fit.predict(start=len(train_X), end=len(train_X)+len(test_X)-1, dynamic=False)

    # Calculer l'erreur quadratique moyenne / Prédire la valeur suivante
    mse = mean_squared_error(test_y, predictions)
    nouvelle_prediction = model_fit.predict(start=len(X), end=len(X)).iloc[0]
    nouvelle_prediction_arrondie = round(nouvelle_prediction, 2)
    return mse, nouvelle_prediction_arrondie

if __name__ == "__main__":
    #csv_path = 'C:\\Users\\lanfr\\Cours Ynov\\B2\\Projet_Dev\\DB\\temperature.csv'
    csv_path = 'DB/temperature.csv'
    mse, nouvelle_prediction_arrondie = Prevision(csv_path)
    print("\n")
    print("Erreur quadratique moyenne :", mse)
    print("Prediction de la valeur suivante :", nouvelle_prediction_arrondie)
