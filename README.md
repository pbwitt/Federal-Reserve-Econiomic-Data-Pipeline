## Data Pipeline Overview

### Key Features:

To me, a successful data pipeline should do the following:

1) Automate data extraction and wrangling. The work is done upfront.  Once code is final, little work is required to maintain it, depending on the data sources.  

2) Produce reusable code so others can access it. Custom python data pull and data wrangle modules make a user friendly API.  This is my preferred method for databases as well.

3) Produce datasets that are optimized for aggregations. In other words, datasets that can be loaded and used for analysis in other applications. I prefer to work with single flat files or data frame objects if resources permit.  Once DataPull functions are written and automated, the focus is primarily on doing analysis.  For this exercise, I automated the extraction and wrangling, and produced flat files that were exported for use in Tableau.  In general, this workflow is used in most data pipelines.  

https://public.tableau.com/views/FREDDASHBOARDM1DataQualityMeasure/MoneyStockMeasureDash?:language=en-US&:display_count=n&:origin=viz_share_link



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

function initializeViz() {
var placeholderDiv = document.getElementById("tableauViz");
var url = "http://public.tableau.com/views/WorldIndicators/GDPpercapita";
var options = {
 width: '600px',
 height: '600px',
 hideTabs: true,
 hideToolbar: true,
 };
viz = new tableau.Viz(placeholderDiv, url, options);
}
