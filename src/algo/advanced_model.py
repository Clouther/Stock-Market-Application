import logging
import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier as DecisionTree
from sklearn.metrics import balanced_accuracy_score as BAS
from sklearn.ensemble import RandomForestClassifier as RandomForest
from sklearn.ensemble import RandomForestClassifier as AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier as GradientBoostingClassifier


def create_features(df_stock, nlags=10):

    """ Focuses on the closing price of a pandas financial dataframe and will shift the dataframe by the number of nlag steps adding a new column for each nlag step

    Parameters:
    df_stock (Pandas Dataframe): Description of arg1
    nlags (int): Number of datapoints we want removed / shifted from our original dataframe

    Returns:
    df: Returns a restructed pandas dataframe with only close price and new columns based on the size of nlags

   """

    df_resampled = df_stock.copy()

    df_resampled['SMA_10'] = df_resampled['close'].rolling(10, min_periods=1).mean()
    df_resampled['SMA_20'] = df_resampled['close'].rolling(20, min_periods=1).mean()
    df_resampled['SMA_50'] = df_resampled['close'].rolling(50, min_periods=1).mean()
    df_resampled['SMA_100'] = df_resampled['close'].rolling(100, min_periods=1).mean()
    df_resampled['SMA_200'] = df_resampled['close'].rolling(200, min_periods=1).mean()
    df_resampled['EMA_12'] = df_resampled['close'].ewm(12, min_periods=1).mean()
    df_resampled['EMA_26'] = df_resampled['close'].ewm(26, min_periods=1).mean()
    df_resampled['EMA_50'] = df_resampled['close'].ewm(50, min_periods=1).mean()

    df_resampled['> SMA_10'] = np.where(df_resampled['close'] > df_resampled['SMA_10'], 1, 0)
    df_resampled['> SMA_20'] = np.where(df_resampled['close'] > df_resampled['SMA_20'], 1, 0)
    df_resampled['> SMA_50'] = np.where(df_resampled['close'] > df_resampled['SMA_50'], 1, 0)
    df_resampled['> SMA_100'] = np.where(df_resampled['close'] > df_resampled['SMA_100'], 1, 0)
    df_resampled['> SMA_200'] = np.where(df_resampled['close'] > df_resampled['SMA_200'], 1, 0)
    df_resampled['> EMA_12'] = np.where(df_resampled['close'] > df_resampled['EMA_12'], 1, 0)
    df_resampled['> EMA_26'] = np.where(df_resampled['close'] > df_resampled['EMA_26'], 1, 0)
    df_resampled['> EMA_50'] = np.where(df_resampled['close'] > df_resampled['EMA_50'], 1, 0)

    df_resampled['Golden Cross'] = np.where(df_resampled['SMA_20'] > df_resampled['SMA_100'], 1, 0)
    df_resampled['Dead Cross'] = np.where(df_resampled['SMA_20'] < df_resampled['SMA_100'], 1, 0)
    df_resampled['MACD'] = np.where(df_resampled['EMA_12'] > df_resampled['EMA_26'], 1, 0)

    lags_col_names = list(df_resampled.columns.values)[15:]

    for i in range(nlags + 1):
        df_resampled['lags_' + str(i)] = df_resampled['close'].diff().shift(i)
        lags_col_names.append('lags_' + str(i))
    df = df_resampled[lags_col_names]
    df = df.dropna(axis=0)

    df['lags_0'] = np.sign(df['lags_0'])
    df['lags_0'] = np.where(df['lags_0'] == 0, 1, df['lags_0'])

    return df


def create_X_Y(df_lags):

    """ Creates the features that will be used in our prediction model

    Parameters:
    df_stock (Pandas Dataframe): Description of arg1
    nlags (int): Number of datapoints we want removed / shifted from our original dataframe

    Returns:
    df: Returns a restructed pandas dataframe with only close price and new columns based on the size of nlags

   """


    X = df_lags.drop('lags_0', axis=1)
    Y = df_lags[['lags_0']]
    return X, Y


class StockModels(BaseEstimator, TransformerMixin):

    def __init__(self, data_fetcher, model_type):
        self.log = logging.getLogger()
        self._data_fetcher = data_fetcher
        self.log.warning('here')
        self._model_type = model_type
        if model_type == 'decision tree':
            self.mod = DecisionTree()
        elif model_type == 'logistic regression':
            self.mod = LogisticRegression()
        elif model_type == 'random forest':
            self.mod = RandomForest()
        elif model_type == 'adaboost':
            self.mod = AdaBoostClassifier()
        elif model_type == 'gradient boost':
            self.mod = GradientBoostingClassifier()

    def fit(self, X, Y=None):
        data = self._data_fetcher(X)
        test_len = len(self._data_fetcher(X, last=True))
        train_len = len(self._data_fetcher(X, last=False))
        df_features = create_features(data.iloc[:train_len-test_len])
        df_features, Y = create_X_Y(df_features)
        self.mod.fit(df_features, Y)
        return self

    def predict(self, X, Y=None):
        data = self._data_fetcher(X, last=True)
        df_features = create_features(data)
        df_features, Y = create_X_Y(df_features)
        predictions = self.mod.predict(df_features)

        #return predictions.flatten()[-1]
        return predictions.flatten()

    def validation_df(self, X, Y=None):
        data = self._data_fetcher(X)
        test_len = len(self._data_fetcher(X, last=True))
        df_features = create_features(data.iloc[:test_len])
        df_features, Y = create_X_Y(df_features)
        predictions = self.mod.predict(df_features)

        Y = Y.reset_index()['lags_0']

        valid_df = pd.concat([Y, pd.DataFrame(predictions)],axis=1)
        valid_df.columns = ['Y_Real', 'Y_Pred']

        return valid_df

    def evaluate(self, X, Y=None):
        predictions = self.predict(X, Y=None)
        data = self._data_fetcher(X, last=True)
        df_features = create_features(data)
        _, Y = create_X_Y(df_features)

        return BAS(predictions, Y)

    def evaluate_df(self, X, Y=None):
        predictions = self.predict(X, Y=None)
        data = self._data_fetcher(X, last=True)
        df_features = create_features(data)
        _, Y = create_X_Y(df_features)

        Y = Y.reset_index()['lags_0']

        pred_df = pd.concat([Y, pd.DataFrame(predictions)],axis=1)
        pred_df.columns = ['Y_Real', 'Y_Pred']

        return pred_df

    def values(self, X, Y=None):
        data = self._data_fetcher(X, last=True)
        df_features = create_features(data)
        X, Y = create_X_Y(df_features)
        return X, Y
