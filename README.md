## Data Pipeline Overview

### Key Features:

To me, a successful dat apipeline should do the following:

1) Automate data extraction and wrangling. The work is done upfront.  Once code is final, little work is required to maintain it.    

2) Produce reusable code so others can use it. Custom python data pull and data wrangle modules make a user friendly API.

3) Produce datasets that are optimized for aggregations. In other words, datasets that can be loaded and used for analysis in other applications. I prefer to work with single flat files or data frame objects if resources permit.  Once DataPull functions are written and automated, the focus is primarily on doing analysis.

For this exercise, I built several custom python modules. These libraries could be made available on gitlabs.  

### Documentation
DataPull:

pull_data():

Pulls data from 3 API endpoints.  Automatically loops through each endpoint, pulls all available data, appends and merges them together.  The result is one raw dataset that can be used for more in-depth analysis, including aggregations and data qualty checks.  

DataWrangle:

Cleans, formats and does other custom aggregations to the data pulled from FRED.  Cleans column headings, creates year and month columns.  This module is created separate from DataPull because there will be a continual need to add new functions in the future.  It is also good to keep raw data in its original format to troubleshoot potential issues.  
functions:

#### clean_data(data)
accepts dataframe object.


#### DQ_H6Measure(data,frequency,season_adj_short,year)

Parameters:
result_set: datframe object.


frequency: string - frequency of data requested: 'Monthly', 'Yearly', etc.


season_adj_short: string- provide seasonal adjustment parameter i.e. "NSA"


# Automation

For automation, I use the python schedule module.  It allows for scheduling jobs at time intervals of the developers choosing. https://schedule.readthedocs.io/en/stable/
