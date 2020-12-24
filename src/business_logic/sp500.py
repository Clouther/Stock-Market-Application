import logging
import pandas as pd
import io

from google.cloud import storage
from datetime import datetime
from datetime import timedelta
from yahoo_fin import stock_info as si
from src.business_logic.process_query import create_business_logic
from sklearn.metrics import balanced_accuracy_score as BAS
from src.IO.storage_tools import upload_csv_to_bucket
from src.IO.storage_tools import upload_csv_val_bucket

log = logging.getLogger()
list_ticker_snp_500 = si.tickers_sp500()


def get_sp500_tickers():
    sp_500 = si.tickers_sp500()
    # Removing problematic tickers: Tickers like BF.B that contain a .
    sp_500 = [x for x in sp_500 if "." not in x]

    return sp_500


def getting_all_predictions():
    bl = create_business_logic()
    tickers = get_sp500_tickers()
    empty_df = pd.DataFrame(columns=['Y_Real', 'Y_Pred'])

    for ticker in tickers:
        try:
            bl = create_business_logic()
            eval_tick = bl.do_eval_df(ticker)
            empty_df = empty_df.append(eval_tick)

        except Exception as e:
            print("Oops!", e.__class__, "occurred.")

    empty_df = empty_df.to_csv(index=True, encoding='utf-8')

    upload_csv_to_bucket(empty_df, bl.get_bucket_name())

    return empty_df


def reading_all_predictions():
    log = logging.getLogger()
    client = storage.Client()

    bl = create_business_logic()
    bucket_name = bl.get_bucket_name()
    b = client.get_bucket(bucket_name)

    for i in range(7):
        try:
            date = datetime.now() - timedelta(days=i)
            date = date.strftime("%Y-%m-%d")
            blob = storage.Blob(f'predictions_{date}', b)

            data = blob.download_as_text()
            data = io.StringIO(data)
            df = pd.read_csv(data, index_col=0, sep=",")

            return df
        except:
            log.warning(f'predictions_{date} not found\n')
    else:
        log.warning(f'Updating predictions on S&P 500')
        new_predictions = getting_all_predictions()

        data_predictions = io.StringIO(new_predictions)
        df_new_predictions = pd.read_csv(data_predictions, index_col=0, sep=",")

        return df_new_predictions


def accuracy_all_predictions():
    accuracy_df = reading_all_predictions()
    accuracy_df = pd.DataFrame(accuracy_df)
    acc_val = BAS(accuracy_df.iloc[:,0], accuracy_df.iloc[:,1])

    return acc_val

## Getting Validation Data

def getting_val_predictions():
    bl = create_business_logic()
    tickers = get_sp500_tickers()
    empty_df = pd.DataFrame(columns=['Y_Real', 'Y_Pred'])

    for ticker in tickers:
        try:
            bl = create_business_logic()
            eval_tick = bl.do_val_df(ticker)
            empty_df = empty_df.append(eval_tick)

        except Exception as e:
            print("Oops!", e.__class__, "occurred.")

    empty_df = empty_df.to_csv(index=True, encoding='utf-8')

    upload_csv_val_bucket(empty_df, bl.get_bucket_name())

    return empty_df


def reading_val_predictions():
    log = logging.getLogger()
    client = storage.Client()

    bl = create_business_logic()
    bucket_name = bl.get_bucket_name()
    b = client.get_bucket(bucket_name)

    for i in range(7):
        try:
            date = datetime.now() - timedelta(days=i)
            date = date.strftime("%Y-%m-%d")
            blob = storage.Blob(f'validations_{date}', b)

            data = blob.download_as_text()
            data = io.StringIO(data)
            df = pd.read_csv(data, index_col=0, sep=",")

            return df
        except:
            log.warning(f'validations_{date} not found\n')
    else:
        log.warning(f'Updating validations on S&P 500')
        new_predictions = getting_val_predictions()

        data_predictions = io.StringIO(new_predictions)
        df_new_predictions = pd.read_csv(data_predictions, index_col=0, sep=",")

        return df_new_predictions


def accuracy_val_predictions():
    accuracy_df = reading_val_predictions()
    accuracy_df = pd.DataFrame(accuracy_df)
    acc_val = BAS(accuracy_df.iloc[:,0], accuracy_df.iloc[:,1])

    return acc_val

