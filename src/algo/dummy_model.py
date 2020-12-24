import logging

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as MSE

def create_features(df_stock, nlags=10):

    """ Focuses on the closing price of a pandas financial dataframe and will shift the dataframe by the number of nlag steps adding a new column for each nlag step

    Parameters:
    df_stock (Pandas Dataframe): Description of arg1
    nlags (int): Number of datapoints we want removed / shifted from our original dataframe

    Returns:
    df: Returns a restructed pandas dataframe with only close price and new columns based on the size of nlags

   """

    df_resampled = df_stock.copy()
    lags_col_names = []
    for i in range(nlags + 1):
        df_resampled['lags_' + str(i)] = df_resampled['close'].shift(i)
        lags_col_names.append('lags_' + str(i))
    df = df_resampled[lags_col_names]
    print(df)
    df = df.dropna(axis=0)

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


class Stock_model(BaseEstimator, TransformerMixin):

    def __init__(self, data_fetcher):
        self.log = logging.getLogger()
        self.lr = LinearRegression()
        self._data_fetcher = data_fetcher
        self.log.warning('here')

    def fit(self, X, Y=None):
        data = self._data_fetcher(X)
        df_features = create_features(data)
        df_features, Y = create_X_Y(df_features)
        self.lr.fit(df_features, Y)
        return self

    def predict(self, X, Y=None):
        #print(X)
        data = self._data_fetcher(X, last=True)
        #print(data)
        df_features = create_features(data)
        #print(df_features)
        df_features, Y = create_X_Y(df_features)
        predictions = self.lr.predict(df_features)

        #return predictions.flatten()[-1]
        return predictions.flatten()

    def evaluate(self, X, Y=None):
        predictions = self.predict(X, Y=None)
        data = self._data_fetcher(X, last=True)
        df_features = create_features(data)
        _, Y = create_X_Y(df_features)

        return MSE(predictions, Y)






