## Data Pipeline Overview

### Key Features:

To me, a successful data pipeline should do the following:

1) Automate data extraction and wrangling. The work is done upfront.  Once code is final, little work is required to maintain it, depending on the data sources.  

2) Produce reusable code so others can access it. Custom python data pull and data wrangle modules make a user friendly API.  This is my preferred method for databases as well.

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




# Data Exploration Tableau

https://public.tableau.com/views/FREDDASHBOARDM1DataQualityMeasure/MoneyStockMeasureDash?:language=en-US&:display_count=n&:origin=viz_share_link

<div class='tableauPlaceholder' id='viz1666747305354' style='position: relative'><noscript><a href='#'><img alt='Federal Reserve Board Economic Data (FRED) ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;FR&#47;FREDDASHBOARDM1DataQualityMeasure&#47;MoneyStockMeasureDash&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='FREDDASHBOARDM1DataQualityMeasure&#47;MoneyStockMeasureDash' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;FR&#47;FREDDASHBOARDM1DataQualityMeasure&#47;MoneyStockMeasureDash&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>       



```python
from IPython.display import Image

Image(url="money-supply.jpeg")
```

# H.6 Money Stock Measures

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
pull_data=dp.DataPull()
```

    DataPull Class Invoked. This is a draft demonstration. Author Paul Witt.  Original Work.



```python
fetch_data=pull_data.data_pull()
```

    pulling all releases
    113 this release id did not read
    finished pulling releaes
    pulling observations



```python
fetch_data.to_csv('../result_set.csv')
```


```python
result_set=pd.read_csv('../result_set.csv')
```

# Explore Data

Pull in the data wrangle module.  These modules are reuseable and can alway be applied to the data pulls.  


```python
import importlib
import DataWrangle as DW
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


```python
results_2022
```


```python
results_2022[['date','calculated_m1','pulled_m1','difference']]
```


```python
# money_market=['DEMDEPNS','MDLNM','CURRNS']
```


```python
fetch_data[fetch_data.series_id=='MDLNM']
```


```python
##Pull all years.  This is a complete dataset.  
#The complete dataset can be sent to Tableau, models or other exporation software.
DW.DataWrangle.DQ_H6Measure(result_set,'Monthly','NSA')
```


```python
DW.DataWrangle.DQ_H6Measure(result_set,'Monthly','NSA').to_csv("../complete_dataset.csv")
```
