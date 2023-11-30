from functions import convert_unix_to_datetime , convert_datetime_to_unix , convert_df
from config import api_key_binance , secret_key_binance
from binance.client import Client
from pybit.unified_trading import HTTP

import time 
from config import api_key_bybit , api_secret_bybit
from pybit.unified_trading import HTTP
import pandas as pd
import numpy as np
import streamlit as st
import datetime
import re


def main():

    # proxies

    
   
    #BINANCE DATA

    ##TIMEFRAMES_BINANCE
    all_timeframes_binance = {
        '1 minute' :   Client.KLINE_INTERVAL_1MINUTE , 
        '3 minutes':   Client.KLINE_INTERVAL_3MINUTE,
        '5 minutes':   Client.KLINE_INTERVAL_5MINUTE,
        '15 minutes':  Client.KLINE_INTERVAL_15MINUTE,
        '30 minutes':  Client.KLINE_INTERVAL_30MINUTE,
        '1 hour'   :   Client.KLINE_INTERVAL_1HOUR, 
        '2 hours'  :   Client.KLINE_INTERVAL_2HOUR , 
        '4 hours'  :   Client.KLINE_INTERVAL_4HOUR , 
        '6 hours'  :   Client.KLINE_INTERVAL_6HOUR ,
        '8 hours'  :   Client.KLINE_INTERVAL_8HOUR,
        '12 hours' :   Client.KLINE_INTERVAL_12HOUR,
        '1 day'    :   Client.KLINE_INTERVAL_1DAY,
        '3 days'   :   Client.KLINE_INTERVAL_3DAY,
        '1 week'   :   Client.KLINE_INTERVAL_1WEEK,
        '1 month'  :   Client.KLINE_INTERVAL_1MONTH

        }

    ##DATA_BINANCE
    all_month_binance = {
            1 :  'Jan' , 	2 :  'Feb',
            3 : 'Mar'	, 4 :  'Apr' , 
            5 : 'May' , 6 : 'June' , 
            7 : 'July' , 8 : 'Aug' , 
            9 : 'Sep' , 10 : 'Oct' , 
            11 : 'Nov' , 12 : 'Dec'
        }

    
    #BYBIT_DATA 

    all_timeframes_bybit = { '1 minute' : 1 ,
                         '3 minutes' : 3 ,
                        '5 minutes' : 5  , 
                        '15 minutes' : 15 ,
                          '30 minutes' : 30  ,
                            '1 hour' : 60 , 
                      '2 hours' : 120 , 
                      '4 hours' : 240 , 
                      '6 hours' : 360 , 
                    
                      '12 hours' : 720 ,
                        '1 day' : 'D' , 
                        
                        '1 week' : 'W' , 
                        '1 month' : 'M'}


    
    
    #PAGE_CONTENT

    

    st.write('Cryptocurrency quotes downloader')

    exchange = st.selectbox('Select exchange: ' , ['Coinmarketcap/YahooFinance' , 'Bybit'])


    if exchange == 'Bybit' :
        cryptocurrencies = st.selectbox("Select cryptocurrency: ", ['BTC/USDT', 'ETH/USDT'])
        timeframes = st.selectbox("Select timeframe of quotes: ",
                     ['1 minute', '3 minutes' , '5 minutes' , '15 minutes' , '30 minutes' , '1 hour' , 
                      '2 hours' , '4 hours' , '6 hours' ,  '12 hours' , '1 day' ,  '1 week' , '1 month' ])
        
        temp_list = cryptocurrencies.split('/')
        cc1   = temp_list[0]
        cc2 = temp_list[1]

    elif exchange == 'Coinmarketcap/YahooFinance' :
        cryptocurrencies = st.selectbox("Select cryptocurrency: ", ['BTC-USD', 'ETH-USD'])
        timeframes = st.selectbox("Select timeframe of quotes: ", 
                      ['1 day' ,  '1 week' , '1 month' ])
        temp_list = cryptocurrencies.split('-')
        cc1   = temp_list[0]
        cc2 = temp_list[1]

        
    


   





    date_start = st.date_input("Start of an interval", datetime.date(2018, 7, 6))
    

    date_end = st.date_input("End of an interval", datetime.date(2019, 7, 6))
    

    # @st.cache_data
    # def load_data_binance(cryptocurrency , timeframes , date_start, date_end ):
        

        
    #     proxies = {
    
    #     'https': '42.112.24.127:8888'
    #     }

    #     #BINANCE API CONNECT
        

    #     client = Client(api_key_binance, secret_key_binance)

              

        
        

    #     date_start_day = int(date_start.day)
    #     date_start_month = int(date_start.month)
    #     date_start_year = date_start.year

    #     date_end_day = int(date_end.day)
    #     date_end_month = int(date_end.month)
    #     date_end_year = date_end.year
                

    #     interval_start = str(date_start_day) + ' ' + all_month_binance[date_start_month] + ', ' + str(date_start_year)
    #     interval_end = str(date_end_day) + ' ' + all_month_binance[date_end_month] + ', ' + str(date_end_year)

               
    #     timeframe = all_timeframes_binance[timeframes]

    #     temp_list = cryptocurrency.split('/')
    #     cc1   = temp_list[0]
    #     cc2 = temp_list[1]

    #     cryptocurrency = "".join(temp_list)

    #     klines =  client.get_historical_klines( cryptocurrency, timeframe , interval_start , interval_end)

        
       

    #     klines_df = pd.DataFrame(klines)

        

    #     klines_df = klines_df[[0 , 1, 2 ,3 ,4 ,5 ,7]]
    #     klines_df.rename(columns={0 : 'Datetime' ,
    #                                1 : 'Open' , 
    #                                2 : 'High' ,
    #                                3 : 'Low' , 
    #                                  4 : 'Close' ,
    #                                    5 : f'Volume{cc1}' , 
    #                                    7 : f'Volume{cc2}'}, inplace=True)
        
    #     convert_unix_to_datetime(klines_df , 'Datetime')
    #     return  klines_df

    @st.cache_data
    def load_data_yahoofinance(cryptocurrency , timeframe , date_start , date_end):
        

        time_frames_yahoo = {
            '1 week' : '1wk' , 
            '1 month' : '1mo' , 
            '1 day' :  '1d'


        }
        
        interval = time_frames_yahoo[timeframe]

        date_start_day = int(date_start.day)
        date_start_month = int(date_start.month)
        date_start_year = int(date_start.year)

        date_end_day = int(date_end.day)
        date_end_month = int(date_end.month)
        date_end_year = int(date_end.year)


        

        interval_start = int( time.mktime( datetime.date( date_start_year , date_start_month , date_start_day ).timetuple() )  ) 
        interval_end =  int( time.mktime( datetime.date( date_end_year , date_end_month , date_end_day ).timetuple() )  ) 

        url = f'https://query1.finance.yahoo.com/v7/finance/download/{cryptocurrency}?period1={interval_start}&period2={interval_end}&interval={interval}&events=history&includeAdjustedClose=true'

        return url 

    
    
    @st.cache_data
    def load_data_bybit(cryptocurrency , timeframes , date_start, date_end ):
        
        #CONNECT_BYBIT
        try :

            session = HTTP(testnet=True  ,
                api_key=api_key_bybit ,
                    api_secret=api_secret_bybit)
        except :
            st.write('Failed to connect to ByBit')


        temp_list = cryptocurrency.split('/')
        cc1   = temp_list[0]
        cc2 = temp_list[1]
        cryptocurrency = "".join(temp_list)


        date_start_day = int(date_start.day)
        date_start_month = int(date_start.month)
        date_start_year = int(date_start.year)

        date_end_day = int(date_end.day)
        date_end_month = int(date_end.month)
        date_end_year = int(date_end.year)


        

        interval_start = int( time.mktime( datetime.date( date_start_year , date_start_month , date_start_day ).timetuple() )  ) * 1000
        interval_end =  int( time.mktime( datetime.date( date_end_year , date_end_month , date_end_day ).timetuple() )  ) * 1000

        klines = session.get_kline(
            category="linear",
            symbol= cryptocurrency,
            interval= all_timeframes_bybit[timeframes],
            start= interval_start,
            end= interval_end,
        )
        df = pd.DataFrame(klines['result']['list'])
        

        if len(df) == 0 : 
        
            st.error('Something went wrong. Perhaps during the specified interval, the cryptocurrency has not yet been traded on this exchange')
            pass

        else :
            
            df.rename(columns={0 : 'Datetime' ,
                                            1 : 'Open' , 
                                            2 : 'High' ,
                                            3 : 'Low' , 
                                                4 : 'Close' ,
                                                5 : f'Volume{cc1}' , 
                                                7 : f'Volume{cc2}'}, inplace=True)

            df['Datetime'] = df['Datetime'].astype('int64')
            df['Datetime'] = df['Datetime'] / 1000
            df = convert_unix_to_datetime(df, 'Datetime')

            return  df

    
       
    
    

    
        



    if st.button('Get quotes'):
        if cryptocurrencies != None and timeframes != None and date_start != None and date_end != None and exchange != None :
            if date_start < date_end :
                


                if exchange == 'Coinmarketcap/YahooFinance' :
                    data = load_data_yahoofinance(cryptocurrencies , timeframes , date_start , date_end )
                    
                    if data is not None :
                        st.success('Quotes were uploaded successfully. To see it , click the buttom')
                        df = pd.read_csv(data)
                        st.write(df)
                    else :
                        st.error('Something went wrong. Please try again')

                elif exchange == 'Bybit' :
                    data = load_data_bybit(cryptocurrencies , timeframes , date_start, date_end )

                    
                    st.success('Quotes were uploaded successfully. To see it , click the buttom')
                    st.dataframe(data)
                    csv = convert_df(data)

                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f'{cc1}_{cc2}_quotes.csv',
                        mime='text/csv', ) 

                    


            #  Выяснить вопрос с тем что будет если надо скачать данные за один день
            elif date_start >= date_end :
                st.error('The beginning of a time interval is greater than its end')


        else :
            st.error('Fill in or check all the input fields')
    



if __name__ == '__main__':
    main()
