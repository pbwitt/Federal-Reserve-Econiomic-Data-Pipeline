
class DataWrangle(object):
    def __init__(self):
        ##print(__name__)
        print("DataWrangle Class Invoked. This is a draft demonstration. Author Paul Witt.  Original Work.")
    #Make return rows a global function.

    def clean_data(data):
        """Function cleans up data - year, month, datetime, and some changes. More will be needed"""
        import pandas as pd
        import datetime


        data.rename(columns={'@realtime_start':'realtime_start','@realtime_end':'realtime_end','@date':'date', '@value':'value'},inplace=True)

        data['date']=pd.to_datetime(data['date'])
        data['year']=data['date'].dt.year
        data['month']=data['date'].dt.month

        #to do: remove bad charaters so float can be converted.
        #data['value']=data.value.astype(float)
    def DQ_H6Measure(data,frequency,season_adj_short,year=None):
        print('run data')

        """This fucntion creates a datasets for Data Quality Measure. Test """
        # filter on component parts
        money_market=['DEMDEPNS','MDLNM','CURRNS']
        import numpy as np
        # create parameter option. Filter on year if available, if not, pull all.
        if year!=None:

            filtered_data=data[(data.name=="H.6 Money Stock Measures")&\
                               (data.frequency==frequency)&\
                               (data.seasonal_adjustment_short==season_adj_short)&(data.year==year)]
        else:
            filtered_data=data[(data.name=="H.6 Money Stock Measures")&\
                                   (data.frequency==frequency)&\
                                   (data.seasonal_adjustment_short==season_adj_short)]


        final_analysis=filtered_data[filtered_data.series_id.isin(money_market)].groupby(['title','series_id','date'])\
        .agg({"value":np.sum}).reset_index()

        final_analysis['value']=final_analysis['value'].astype(float)

        # filer on M1.  This is the data aggregate pulled directly from the API.  Used to compare against componets,
        M1=filtered_data[filtered_data.series_id=='M1NS'].groupby(['title','series_id','date']).agg({"value":np.sum}).reset_index()
        M1.rename(columns={'value':'pulled_m1'},inplace=True)


        M1.pulled_m1=M1.pulled_m1.astype(float)

        pivot1=final_analysis.pivot(index='date',columns='title',values='value')

        final_pivot=pivot1.reset_index()
        final_pivot['calculated_m1']=final_pivot.iloc[:, 1:].sum(axis=1)

        final_subtraction=final_pivot.merge(M1[['date','pulled_m1']],how='inner',on="date")
        final_subtraction['difference']=final_subtraction.iloc[:, -2]-final_subtraction.iloc[:, -1]


        return final_subtraction
