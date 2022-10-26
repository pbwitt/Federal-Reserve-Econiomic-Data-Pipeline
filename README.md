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

<div class='tableauPlaceholder' id='viz1666746333735' style='position: relative'><noscript><a href='#'><img alt='M1 Time Series ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;FR&#47;FREDDASHBOARD&#47;M1TimeSeries&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='FREDDASHBOARD&#47;M1TimeSeries' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;FR&#47;FREDDASHBOARD&#47;M1TimeSeries&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1666746333735');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else { vizElement.style.width='100%';vizElement.style.height='877px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
