## Data Pipeline Overview

### Key Features:

To me, a successful data pipeline should do the following:

1) Automate data extraction and wrangling. The work is done upfront.  Once code is final, little work is required to maintain it, depending on the data sources.  

2) Produce reusable code so others can access it. Custom python data pull and data wrangle modules make a user friendly API.  Creating useful paramters makes working with data much easier for analysis.  This is my preferred method for databases as well.

3) Produce datasets that are optimized for aggregations. In other words, datasets that can be loaded and used for analysis in other applications. I prefer to work with single flat files or data frame objects if resources permit.  Once DataPull functions are written and automated, the focus is primarily on doing analysis.  For this exercise, I automated the extraction and wrangling, and produced flat files that were exported for use in Tableau.  In general, this workflow is used in most data pipelines.  





https://public.tableau.com/app/profile/paul.witt2290/viz/FREDDASHBOARD/M1TimeSeries

For this exercise, I built several custom python modules. These modules could be made available on gitlabs.  


### Documentation
DataPull:
class DataPull.pull_data()

Pulls data from FRED API endpoints.  Automatically loops through each endpoint, pulls all available data, appends and merges them together as appropriate.  The result is one raw dataset that can be used for more in-depth analysis, including aggregations, data quality checks, and model inputs.  Also useful for stakeholders who just want raw data.

returns dataframe object of raw data.    

DataWrangle:

Cleans, formats and does other custom aggregations to the data pulled from FRED.  Cleans column headings, creates year and month columns.  This module is created separate from DataPull because there will be a continual need to add new functions in the future.  It is also good to keep raw data in its original format to troubleshoot and understand potential data issues.  
functions:

#### clean_data(data)
accepts dataframe object.  Cleans column headings, creates year and month columns.  


#### DQ_H6Measure(data,frequency,season_adj_short,year)

Parameters:
data: DataFrame object.

frequency: string - frequency of data requested: 'Monthly', 'Yearly', etc.

season_adj_short: string- provide seasonal adjustment parameter i.e. "NSA"

year: calendar year, default is None. Will return all years.

# Automation

For automation, I use the python schedule module.  It allows for scheduling jobs at time intervals of the developers choosing. https://schedule.readthedocs.io/en/stable/

The automation script incorporates different checks to help troubleshoot potential data issues.  Larger pulls can be scheduled at night or early morning.  Runs from terminal on windows, mac or linux

![alt text](https://github.com/pbwitt/Federal-Reserve-Econiomic-Data-Pipeline/blob/main/Automation%20Terminal%20.png)






```python
from IPython.display import Image

Image(url="money-supply.jpeg")
```




<img src="money-supply.jpeg"/>




```python
import xmltodict
import requests
#df = pd.DataFrame(dict_data, columns=dict_data.keys())

#observations=pd.DataFrame(dict_data.get('observations', {}).get('observation'))
#observations['series_id']=str(v)

#appended_data_2.append(observations)
```


```python
series_id_money=['MDLNM','CURRNS','M1NS']
appended_data_2 = []
import pandas as pd
try:
    for x ,v  in enumerate(series_id_money):
                #print(len(unique_series_id_list))
        #print('https://api.stlouisfed.org/fred/series/observations?series_id='+v+'&api_key=d0640df392d50e841ab2e3c22bf258ed')
        obervations = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id='+v+'&api_key=d0640df392d50e841ab2e3c22bf258ed')
        

        dict_data = xmltodict.parse(obervations.content)
        df = pd.DataFrame(dict_data, columns=dict_data.keys())

        observations=pd.DataFrame(dict_data.get('observations', {}).get('observation'))
        observations['series_id']=str(v)

        appended_data_2.append(observations)
        #print(appended_data_2)
        
except:
    print(str(v) + " this series id did not read")
    pass

observations_data = pd.concat(appended_data_2)       
        
```


```python
observations_data.series_id.unique()
```




    array(['MDLNM', 'CURRNS', 'M1NS'], dtype=object)



# Data Wrangling and Analysis



### H.6 Money Stock Measures Data Requirements

An Analysis presented to the Federal Reserve Board 

Tasks to be completed:

Using the St. Louis FRED API, pull data on monthly, non-seasonally adjusted M1 and its sub-components from January 2022 through August 2022, inclusive. 

M1 is one of two money stock measures MPOA publishes on the H.6 statistical release.
The sub-components of M1 include currency, demand deposits, and other liquid deposits.

Data on monthly, non-seasonally adjusted M1 and its sub-components can be referenced from FRED’s H.6 Money Stock Measure, Release Table 3 (https://fred.stlouisfed.org/release/tables?rid=21&eid=1217611). 

Calculate M1 for each month in the above range by summing, for a given month, the M1 sub-components. 
Create an output CSV with the following information:


Col 1:  Date of M1 observation in yyyy-mm format

Col 2:  Pulled monthly, non-seasonally adjusted M1 value in $billions from FRED

Col 3:  Calculated monthly, non-seasonally adjusted M1 value in $billions constructed from M1 sub-components pulled from FRED

Col 4:  Difference between column 2 and column 3 values in $billions

We are expecting an output CSV containing nine rows (one row of labels and eight rows of M1 data) and four columns.  An example of the expected output for December 2021 would look like: 

date, pulled_m1, calculated_m1, difference


```python
import DataPull as dp
import pandas as pd
```


```python
fetch=dp.DataPull()
```

    DataPull Class Invoked. This is a draft demonstration. Author Paul Witt.  Original Work.



```python
result_set=fetch.data_pull()
```

    pulling all releases
    pulling observations
                       observations
    @count                      765
    @file_type                  xml
    @limit                   100000
    @observation_end     9999-12-31
    @observation_start   1600-01-01
                       observations
    @count                      765
    @file_type                  xml
    @limit                   100000
    @observation_end     9999-12-31
    @observation_start   1600-01-01
                       observations
    @count                       29
    @file_type                  xml
    @limit                   100000
    @observation_end     9999-12-31
    @observation_start   1600-01-01
                       observations
    @count                      909
    @file_type                  xml
    @limit                   100000
    @observation_end     9999-12-31
    @observation_start   1600-01-01
    finished observations...merging datasets



```python
result_set.series_id.unique()
```




    array(['M1NS', 'DEMDEPNS', 'MDLNM', 'CURRNS'], dtype=object)




```python
result_set
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>@realtime_start</th>
      <th>@realtime_end</th>
      <th>@date</th>
      <th>@value</th>
      <th>series_id</th>
      <th>id_x</th>
      <th>realtime_start</th>
      <th>realtime_end</th>
      <th>title</th>
      <th>observation_start</th>
      <th>...</th>
      <th>units_short</th>
      <th>seasonal_adjustment</th>
      <th>seasonal_adjustment_short</th>
      <th>last_updated</th>
      <th>popularity</th>
      <th>group_popularity</th>
      <th>notes</th>
      <th>release_id</th>
      <th>id_y</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>1959-01-01</td>
      <td>142.2</td>
      <td>M1NS</td>
      <td>M1NS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>M1</td>
      <td>1959-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:12-05</td>
      <td>55</td>
      <td>89</td>
      <td>Before May 2020, M1 consists of (1) currency o...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>1959-02-01</td>
      <td>139.3</td>
      <td>M1NS</td>
      <td>M1NS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>M1</td>
      <td>1959-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:12-05</td>
      <td>55</td>
      <td>89</td>
      <td>Before May 2020, M1 consists of (1) currency o...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>1959-03-01</td>
      <td>138.4</td>
      <td>M1NS</td>
      <td>M1NS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>M1</td>
      <td>1959-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:12-05</td>
      <td>55</td>
      <td>89</td>
      <td>Before May 2020, M1 consists of (1) currency o...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>1959-04-01</td>
      <td>139.7</td>
      <td>M1NS</td>
      <td>M1NS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>M1</td>
      <td>1959-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:12-05</td>
      <td>55</td>
      <td>89</td>
      <td>Before May 2020, M1 consists of (1) currency o...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>1959-05-01</td>
      <td>138.7</td>
      <td>M1NS</td>
      <td>M1NS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>M1</td>
      <td>1959-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:12-05</td>
      <td>55</td>
      <td>89</td>
      <td>Before May 2020, M1 consists of (1) currency o...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2463</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>2022-05-01</td>
      <td>2180.9</td>
      <td>CURRNS</td>
      <td>CURRNS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>Currency Component of M1</td>
      <td>1947-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:18-05</td>
      <td>40</td>
      <td>61</td>
      <td>The currency component of M1, sometimes called...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>2464</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>2022-06-01</td>
      <td>2184.1</td>
      <td>CURRNS</td>
      <td>CURRNS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>Currency Component of M1</td>
      <td>1947-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:18-05</td>
      <td>40</td>
      <td>61</td>
      <td>The currency component of M1, sometimes called...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>2465</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>2022-07-01</td>
      <td>2185.4</td>
      <td>CURRNS</td>
      <td>CURRNS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>Currency Component of M1</td>
      <td>1947-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:18-05</td>
      <td>40</td>
      <td>61</td>
      <td>The currency component of M1, sometimes called...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>2466</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>2022-08-01</td>
      <td>2186.2</td>
      <td>CURRNS</td>
      <td>CURRNS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>Currency Component of M1</td>
      <td>1947-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:18-05</td>
      <td>40</td>
      <td>61</td>
      <td>The currency component of M1, sometimes called...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>2467</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>2022-09-01</td>
      <td>2188.5</td>
      <td>CURRNS</td>
      <td>CURRNS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>Currency Component of M1</td>
      <td>1947-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:18-05</td>
      <td>40</td>
      <td>61</td>
      <td>The currency component of M1, sometimes called...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
  </tbody>
</table>
<p>2468 rows × 24 columns</p>
</div>




```python
result_set[result_set.series_id=='M1NS'].head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>@realtime_start</th>
      <th>@realtime_end</th>
      <th>@date</th>
      <th>@value</th>
      <th>series_id</th>
      <th>id_x</th>
      <th>realtime_start</th>
      <th>realtime_end</th>
      <th>title</th>
      <th>observation_start</th>
      <th>...</th>
      <th>units_short</th>
      <th>seasonal_adjustment</th>
      <th>seasonal_adjustment_short</th>
      <th>last_updated</th>
      <th>popularity</th>
      <th>group_popularity</th>
      <th>notes</th>
      <th>release_id</th>
      <th>id_y</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>1959-01-01</td>
      <td>142.2</td>
      <td>M1NS</td>
      <td>M1NS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>M1</td>
      <td>1959-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:12-05</td>
      <td>55</td>
      <td>89</td>
      <td>Before May 2020, M1 consists of (1) currency o...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>1959-02-01</td>
      <td>139.3</td>
      <td>M1NS</td>
      <td>M1NS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>M1</td>
      <td>1959-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:12-05</td>
      <td>55</td>
      <td>89</td>
      <td>Before May 2020, M1 consists of (1) currency o...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>1959-03-01</td>
      <td>138.4</td>
      <td>M1NS</td>
      <td>M1NS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>M1</td>
      <td>1959-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:12-05</td>
      <td>55</td>
      <td>89</td>
      <td>Before May 2020, M1 consists of (1) currency o...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>1959-04-01</td>
      <td>139.7</td>
      <td>M1NS</td>
      <td>M1NS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>M1</td>
      <td>1959-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:12-05</td>
      <td>55</td>
      <td>89</td>
      <td>Before May 2020, M1 consists of (1) currency o...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>1959-05-01</td>
      <td>138.7</td>
      <td>M1NS</td>
      <td>M1NS</td>
      <td>2022-10-26</td>
      <td>2022-10-26</td>
      <td>M1</td>
      <td>1959-01-01</td>
      <td>...</td>
      <td>Bil. of $</td>
      <td>Not Seasonally Adjusted</td>
      <td>NSA</td>
      <td>2022-10-25 14:23:12-05</td>
      <td>55</td>
      <td>89</td>
      <td>Before May 2020, M1 consists of (1) currency o...</td>
      <td>21</td>
      <td>21</td>
      <td>H.6 Money Stock Measures</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 24 columns</p>
</div>




```python
series_id_money=['DEMDEPNS','MDLNM','CURRNS','M1NS']
```


```python
#result_set.to_csv('../result_set.csv')
```


```python

```


```python
#result_set=pd.read_csv('../result_set.csv')
```

# Explore Data

Pull in the data wrangle module.  These modules are reuseable and can alway be applied to the data pulls.  


```python
import importlib
import DataWrangle as DW
```


```python
series=result_set['series_id'].unique().tolist()
```


```python
#importlib.reload(DW)
```

Apply data clean module. Adds Month Year.  Should chage data types as well.  
There are records with non-integers in the vlaue column.  Requires more work to clean 


```python
#before 
result_set.columns
```




    Index(['@realtime_start', '@realtime_end', '@date', '@value', 'series_id',
           'id_x', 'realtime_start', 'realtime_end', 'title', 'observation_start',
           'observation_end', 'frequency', 'frequency_short', 'units',
           'units_short', 'seasonal_adjustment', 'seasonal_adjustment_short',
           'last_updated', 'popularity', 'group_popularity', 'notes', 'release_id',
           'id_y', 'name'],
          dtype='object')




```python
#After
DW.DataWrangle.clean_data(result_set)
```


```python
##apply data quality function. Takes in parameters that allows the logic to be applied to series from Fred. 
## Lots more could be done to customize this function.  # I call it a data quality function because I assume that is \
# what it is trying to achieve.  
```


```python
## The function accepts parameters. very convient for others to use.  Very useful for filtering data.  
# Currently fuction only filters on NSA but that could be altered.   
results_2022=DW.DataWrangle.DQ_H6Measure(result_set,'Monthly','NSA',2022)
```

    run DQ measure



```python
results_2022
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>Currency Component of M1</th>
      <th>Demand Deposits</th>
      <th>Other Liquid Deposits: Total</th>
      <th>calculated_m1</th>
      <th>pulled_m1</th>
      <th>difference</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2022-01-01</td>
      <td>2134.1</td>
      <td>4758.0</td>
      <td>13657.3</td>
      <td>20549.4</td>
      <td>20549.3</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2022-02-01</td>
      <td>2142.3</td>
      <td>4691.7</td>
      <td>13694.0</td>
      <td>20528.0</td>
      <td>20528.1</td>
      <td>-0.1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2022-03-01</td>
      <td>2165.3</td>
      <td>4811.9</td>
      <td>13823.6</td>
      <td>20800.8</td>
      <td>20800.8</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2022-04-01</td>
      <td>2175.7</td>
      <td>4878.8</td>
      <td>13765.5</td>
      <td>20820.0</td>
      <td>20820.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2022-05-01</td>
      <td>2180.9</td>
      <td>4934.5</td>
      <td>13429.5</td>
      <td>20544.9</td>
      <td>20544.8</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2022-06-01</td>
      <td>2184.1</td>
      <td>4949.4</td>
      <td>13413.6</td>
      <td>20547.1</td>
      <td>20547.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2022-07-01</td>
      <td>2185.4</td>
      <td>4965.8</td>
      <td>13337.1</td>
      <td>20488.3</td>
      <td>20488.3</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2022-08-01</td>
      <td>2186.2</td>
      <td>5189.7</td>
      <td>13024.1</td>
      <td>20400.0</td>
      <td>20400.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2022-09-01</td>
      <td>2188.5</td>
      <td>5119.5</td>
      <td>12941.4</td>
      <td>20249.4</td>
      <td>20249.4</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
results_2022[['date','calculated_m1','pulled_m1','difference']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>calculated_m1</th>
      <th>pulled_m1</th>
      <th>difference</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2022-01-01</td>
      <td>20549.4</td>
      <td>20549.3</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2022-02-01</td>
      <td>20528.0</td>
      <td>20528.1</td>
      <td>-0.1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2022-03-01</td>
      <td>20800.8</td>
      <td>20800.8</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2022-04-01</td>
      <td>20820.0</td>
      <td>20820.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2022-05-01</td>
      <td>20544.9</td>
      <td>20544.8</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2022-06-01</td>
      <td>20547.1</td>
      <td>20547.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2022-07-01</td>
      <td>20488.3</td>
      <td>20488.3</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2022-08-01</td>
      <td>20400.0</td>
      <td>20400.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2022-09-01</td>
      <td>20249.4</td>
      <td>20249.4</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python
##Pull all years.  This is a complete dataset.  
#The complete dataset can be sent to Tableau, models or other exporation software. 
DW.DataWrangle.DQ_H6Measure(result_set,'Monthly','NSA')
```

    run DQ measure





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>Currency Component of M1</th>
      <th>Demand Deposits</th>
      <th>Other Liquid Deposits: Total</th>
      <th>calculated_m1</th>
      <th>pulled_m1</th>
      <th>difference</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1959-01-01</td>
      <td>28.4</td>
      <td>113.4</td>
      <td>NaN</td>
      <td>141.8</td>
      <td>142.2</td>
      <td>-0.4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1959-02-01</td>
      <td>28.2</td>
      <td>110.8</td>
      <td>NaN</td>
      <td>139.0</td>
      <td>139.3</td>
      <td>-0.3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1959-03-01</td>
      <td>28.3</td>
      <td>109.8</td>
      <td>NaN</td>
      <td>138.1</td>
      <td>138.4</td>
      <td>-0.3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1959-04-01</td>
      <td>28.3</td>
      <td>111.1</td>
      <td>NaN</td>
      <td>139.4</td>
      <td>139.7</td>
      <td>-0.3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1959-05-01</td>
      <td>28.5</td>
      <td>109.8</td>
      <td>NaN</td>
      <td>138.3</td>
      <td>138.7</td>
      <td>-0.4</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>760</th>
      <td>2022-05-01</td>
      <td>2180.9</td>
      <td>4934.5</td>
      <td>13429.5</td>
      <td>20544.9</td>
      <td>20544.8</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>761</th>
      <td>2022-06-01</td>
      <td>2184.1</td>
      <td>4949.4</td>
      <td>13413.6</td>
      <td>20547.1</td>
      <td>20547.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>762</th>
      <td>2022-07-01</td>
      <td>2185.4</td>
      <td>4965.8</td>
      <td>13337.1</td>
      <td>20488.3</td>
      <td>20488.3</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>763</th>
      <td>2022-08-01</td>
      <td>2186.2</td>
      <td>5189.7</td>
      <td>13024.1</td>
      <td>20400.0</td>
      <td>20400.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>764</th>
      <td>2022-09-01</td>
      <td>2188.5</td>
      <td>5119.5</td>
      <td>12941.4</td>
      <td>20249.4</td>
      <td>20249.4</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>765 rows × 7 columns</p>
</div>




```python
#DW.DataWrangle.DQ_H6Measure(result_set,'Monthly','NSA').to_csv("../complete_dataset.csv")
```


# Data Exploration Tableau

https://public.tableau.com/views/FREDDASHBOARDM1DataQualityMeasure/MoneyStockMeasureDash?:language=en-US&:display_count=n&:origin=viz_share_link

<div class='tableauPlaceholder' id='viz1666747305354' style='position: relative'><noscript><a href='#'><img alt='Federal Reserve Board Economic Data (FRED) ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;FR&#47;FREDDASHBOARDM1DataQualityMeasure&#47;MoneyStockMeasureDash&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='FREDDASHBOARDM1DataQualityMeasure&#47;MoneyStockMeasureDash' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;FR&#47;FREDDASHBOARDM1DataQualityMeasure&#47;MoneyStockMeasureDash&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div> 


```python

```
