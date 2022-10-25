class DataPull(object):
    def __init__(self):
        #print(__name__)
        print("DataPull Class Invoked. This is a draft demonstration. Author Paul Witt.  Original Work.")
    #Make return rows a global function.
    def data_pull(self):

        import xmltodict
        import requests
        import json
        import requests
        import pandas as pd

        #pulls from three API Endpoints
        #to do: add api Key as parameter

        api_key='api_key=d0640df392d50e841ab2e3c22bf258ed'
        releases = requests.get('https://api.stlouisfed.org/fred/releases?api_key=d0640df392d50e841ab2e3c22bf258ed&file_type=json')
        series = requests.get('https://api.stlouisfed.org/fred/category/series?&api_key=d0640df392d50e841ab2e3c22bf258ed&file_type=json')
        #obervations = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=CURRNS&api_key=d0640df392d50e841ab2e3c22bf258ed')
        #had issues with the obervations requets json.  pulled xml to save time.
        #load Json file
        releases = json.loads(releases.text)
        series = json.loads(series.text)

        #put releases json into dataframe.
        releases_df=pd.DataFrame(releases)
        #normalize last column - this is the data we really need.
        releases_df=pd.json_normalize(releases_df.releases)
        #create a unique list of release ids.  This will be used to loop through all series.
        release_id_unique_list=releases_df.id.unique().tolist()



        print('pulling all releases')
        release_dataset = []
        # enumerate through all the release series.
        #It uses a unique list of release id, loops through them individually and puts them into one dataset.
        try:
            for x ,v  in enumerate(release_id_unique_list):
                #print(v)
                series_relese_id=requests.get('https://api.stlouisfed.org/fred/release/series?release_id='+ str(v) +'&'+str(api_key)+'&file_type=json')
                series_relese_id = json.loads(series_relese_id.text)
                series_relese_id=pd.DataFrame(series_relese_id)
                series_relese_id_2=pd.json_normalize(series_relese_id.seriess)
                series_relese_id_2['release_id']=v #add series ID back to file this will be needed to merge with ohter datasets.
                release_dataset.append(series_relese_id_2)
        except:
            #if
            print(str(v) + " this release id did not read")
            pass

        release_dataset = pd.concat(release_dataset)
        print('finished pulling releaes')

        unique_series_id_list=release_dataset.id.unique().tolist()

        appended_data_2 = []
        seriesc=[]

        print('pulling observations')
        #fetches the obersvation data. loops thorugh each obersvation set by inserting the series id in.

        try:
            for x ,v  in enumerate(unique_series_id_list):
                #print(len(unique_series_id_list))

                obervations = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id='+v+'&api_key=d0640df392d50e841ab2e3c22bf258ed')
                dict_data = xmltodict.parse(obervations.content)
                df = pd.DataFrame(dict_data, columns=dict_data.keys())

                observations=pd.DataFrame(dict_data.get('observations', {}).get('observation'))
                observations['series_id']=str(v)

                appended_data_2.append(observations)
                seriesc.append(v)

        except:
            print(str(v) + " this series id did not read")
            pass

        observations_data = pd.concat(appended_data_2)

        print('finished observations...merging datasets')

        release_series=release_dataset.merge(releases_df[['id','name']],how='inner',right_on='id',left_on='release_id')
        final_result_set=observations_data.merge(release_series,left_on='series_id',right_on='id_x')

        return final_result_set
