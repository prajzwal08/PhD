variables = [‘Total evaporation’,’Volumetric soil water layer 1’,’Volumetric soil water layer 2’,’Volumetric soil water layer 3’,’Volumetric soil water layer 4’]import itertools
import cdsapi
import os 

output_dir = "output"

c = cdsapi.Client()

variables = ['2m_temperature' , 'total_precipitation', '2m_dewpoint_temperature',
            'surface_pressure', 'surface_solar_radiation_downwards',
            'surface_thermal_radiation_downwards','10m_u_component_of_wind',
            '10m_v_component_of_wind']

years = list(range(2012, 2023))            
#years = [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
location = [50.681189,2.932320,53.915328,7.347674]

for var, year, month in itertools.product(variables, years, months):
    # Create an "output" directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a folder for each variable inside "output"
    var_folder = os.path.join(output_dir, f"{var}")
    os.makedirs(var_folder, exist_ok=True)

    # Construct the output file path with the variable name inside "output"
    output_file_path = os.path.join(var_folder, f"era5-land_{var}_{year}-{month}.nc")
    
    c.retrieve(
        "reanalysis-era5-land",
        {
            "variable": [var],
            "year": f"{year}",
            "month": month,
            "day": [
                "01", "02", "03",
                "04", "05", "06",
                "07", "08", "09",
                "10", "11", "12",
                "13", "14", "15",
                "16", "17", "18",
                "19", "20", "21",
                "22", "23", "24",
                "25", "26", "27",
                "28", "29", "30",
                "31",
            ],
            "time": [
                "00:00", "01:00", "02:00",
                "03:00", "04:00", "05:00",
                "06:00", "07:00", "08:00",
                "09:00", "10:00", "11:00",
                "12:00", "13:00", "14:00",
                "15:00", "16:00", "17:00",
                "18:00", "19:00", "20:00",
                "21:00", "22:00", "23:00",
            ],
            'area': location,
            "format": "netcdf",
        },
         output_file_path
    )
