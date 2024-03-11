import itertools
import cdsapi
import os 
import yaml

output_dir = '/home/khanalp/task1/data/cams'

with open ('/home/khanalp/.adsapirc', 'r') as f:
    credentials= yaml.safe_load(f)
    
c = cdsapi.Client(url=credentials['url'], key=credentials['key'])


variables = ['carbon_dioxide']

#years = list(range(2012, 2013))            
#years = [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]
#months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
#location = [35.8149, -25.0, 71.1851, 44.7909] 

c.retrieve(
    'cams-global-ghg-reanalysis-egg4',
    {
        'variable': 'carbon_dioxide',
        'model_level': '60',
        'date': '2012-01-01/2020-12-31',
        'step': '3',
        'area': [
            71.18, -25, 35.81,
            44.79,
        ],
        'format': 'netcdf',
    },
    os.path.join(output_dir,f'cams.nc')
)
