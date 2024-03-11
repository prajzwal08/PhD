import itertools
import cdsapi
import os 
import pandas as pd
import numpy as np

c = cdsapi.Client()

output_dir = "/home/khanalp/task1/data/ESACCILCCS"

date_range = pd.date_range(np.datetime64("1992-01-01"), np.datetime64("2020-12-31"))
year_month_pairs = [(str(date.year), str(date.month)) for date in date_range]

years = {year for (year, _) in year_month_pairs}

for year in years:
    if int(year) < 2016:
        version = "v2.0.7cds"
    else:
        version = "v2.1.1"
        
    r = c.retrieve(
        "satellite-land-cover",
        {
            "variable": "all",
            "format": "zip",
            "year": year,
            "version": version,
        },
        os.path.join(output_dir, f"ESACCI_LCCS_MAP_300m_{year}.zip")    
    )