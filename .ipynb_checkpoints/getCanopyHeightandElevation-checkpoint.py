import ee
import pandas as pd
import os
import xarray as xr


ee.Initialize()

stations = pd.read_excel("Stationdetails.xlsx")
stations.rename(columns={'Position (lon,lat)': 'Position'}, inplace=True)
# Initialize an empty dictionary to store station_name, latitude, and longitude
station_coordinates = {}

# Iterate over each row in the DataFrame
for index, row in stations.iterrows():
    # Extract the station_name and position
    station_name = row['station_name']
    position = row['Position']
    
    # Split the position string to get latitude and longitude
    longitude, latitude = map(float, position.split(','))
    
    # Store the station_name, latitude, and longitude in the dictionary
    station_coordinates[station_name] = {'latitude': latitude, 'longitude': longitude}

# Create an image collection for MODIS LAI data
dem_collection = ee.ImageCollection("COPERNICUS/DEM/GLO30") 
canopy_height = ee.Image('users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1')
sd_canopy = ee.Image('users/nlang/ETH_GlobalCanopyHeightSD_2020_10m_v1')

# Initialize lists to store data
station_names = []
latitudes = []
longitudes = []
elevations = []
height_canopies = []
sd_height_canopies = []

# Iterate over each station in the dictionary
for station_name, coordinates in station_coordinates.items():
    # Extract latitude and longitude for the station
    latitude = coordinates['latitude']
    longitude = coordinates['longitude']
    
    # Define the location (longitude, latitude)
    point = ee.Geometry.Point(longitude, latitude)
    
    #Get dem
    dem = dem_collection.filterBounds(point).first()
    #Get the elevation value at the specified point
    elevation = dem.sample(target_location, 30).first().get('DEM').getInfo()
    # Sample the canopy height image at the target location
    height_canopy = canopy_height.sample(target_location, 10).first().get('b1').getInfo()  
    sd_height_canopy = sd_canopy.sample(target_location, 10).first().get('b1').getInfo()
    
    # Append data to lists
    station_names.append(station_name)
    latitudes.append(latitude)
    longitudes.append(longitude)
    elevations.append(elevation)
    height_canopies.append(height_canopy)
    sd_height_canopies.append(sd_height_canopy)

    break 

# Create DataFrame
df = pd.DataFrame({
    'station_name': station_names,
    'latitude': latitudes,
    'longitude': longitudes,
    'elevation': elevations,
    'height_canopy': height_canopies,
    'sd_height_canopy': sd_height_canopies
})

#Save this csv
df.to_csv('station_with_elevation_heightcanopy.csv', index=False)



