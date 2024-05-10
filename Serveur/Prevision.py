import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error

def Prevision_Temperature(csv_path, lag=3):
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

def Prevision_Humidite(csv_path, lag=3):
    data = pd.read_csv(csv_path)
    X = data.iloc[:, -1].to_frame()

    for i in range(1, lag + 1):
        X[f'lag_{i}'] = X['Humidite'].shift(i)

    X.dropna(inplace=True)
    train_size = int(len(X) * 0.8)
    humidite_train, humidite_test = X[0:train_size], X[train_size:]
    humidite_train_X, humidite_train_y = humidite_train.drop(columns=['Humidite']), humidite_train['Humidite']
    humidite_test_X, humidite_test_y = humidite_test.drop(columns=['Humidite']), humidite_test['Humidite']
    model = AutoReg(humidite_train_y, lags=lag)
    model_fit = model.fit()
    predictions = model_fit.predict(start=len(humidite_train_X), end=len(humidite_train_X)+len(humidite_test_X)-1, dynamic=False)
    mse = mean_squared_error(humidite_test_y, predictions)
    nouvelle_prediction = model_fit.predict(start=len(X), end=len(X)).iloc[0]
    nouvelle_prediction_arrondie = round(nouvelle_prediction, 2)
    return mse, nouvelle_prediction_arrondie

def Prevision_Luminosite(csv_path, lag=3):
    data = pd.read_csv(csv_path)
    X = data.iloc[:, -1].to_frame()

    for i in range(1, lag + 1):
        X[f'lag_{i}'] = X['Luminosite'].shift(i)

    X.dropna(inplace=True)
    train_size = int(len(X) * 0.8)
    luminosite_train, luminosite_test = X[0:train_size], X[train_size:]
    luminosite_train_X, luminosite_train_y = luminosite_train.drop(columns=['Luminosite']), luminosite_train['Luminosite']
    luminosite_test_X, luminosite_test_y = luminosite_test.drop(columns=['Luminosite']), luminosite_test['Luminosite']
    model = AutoReg(luminosite_train_y, lags=lag)
    model_fit = model.fit()
    predictions = model_fit.predict(start=len(luminosite_train_X), end=len(luminosite_train_X)+len(luminosite_test_X)-1, dynamic=False)
    mse = mean_squared_error(luminosite_test_y, predictions)
    nouvelle_prediction = model_fit.predict(start=len(X), end=len(X)).iloc[0]
    nouvelle_prediction_arrondie = round(nouvelle_prediction, 2)
    return mse, nouvelle_prediction_arrondie

if __name__ == "__main__":
    # Chemin vers le fichier CSV / Prévision
    csv_path_temperature = 'Serveur/DB/temperature.csv'
    mse_temperature, nouvelle_prediction_temperature = Prevision_Temperature(csv_path_temperature)
    print("\n")
    print("----------")
    print("Prevision_Temperature")
    print("Erreur quadratique moyenne :", mse_temperature)
    print("Prediction de la valeur suivante :", nouvelle_prediction_temperature)
    print("----------")
    print("\n")
    
    # Chemin vers le fichier CSV / Prévision
    csv_path_humidite = 'Serveur/DB/humidite.csv'
    mse_humidite, nouvelle_prediction_humidite = Prevision_Humidite(csv_path_humidite)
    print("\n")
    print("----------")
    print("Prevision_Humidite")
    print("Erreur quadratique moyenne :", mse_humidite)
    print("Prediction de la valeur suivante :", nouvelle_prediction_humidite)
    print("----------")
    print("\n")

    '''
    # Chemin vers le fichier CSV / Prévision
    csv_path_luminosite = 'Serveur/DB/luminosite.csv'
    mse_luminosite, nouvelle_prediction_luminosite = Prevision_Luminosite(csv_path_luminosite)
    print("\n")
    print("----------")
    print("Prevision_Luminosite")
    print("Erreur quadratique moyenne :", mse_luminosite)
    print("Prediction de la valeur suivante :", nouvelle_prediction_luminosite)
    print("----------")
    print("\n")
    '''

