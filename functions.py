import pandas as pd 
from datetime import date
import time 


def convert_unix_to_datetime(df, column):
        df[column] = df[column] / 1000
        df[column] = pd.to_datetime(df[column], unit='s')
        return df


def convert_df(df):
        return df.to_csv().encode('utf-8')


def convert_datetime_to_unix(year , month , date):
        d = date(year , month , date)
        unix = time.mktime(d.timetuple())
        unix = int(unix) * 1000
        return unix 

        
        

