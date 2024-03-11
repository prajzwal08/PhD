import ee
import pandas as pd

ee.Initialize()

stations = pd.read_csv("/home/khanalp/task1/output/Stationdetails.csv")

# Initialize an empty dictionary to store station_name, latitude, and longitude
station_coordinates = {}

# Iterate over each row in the DataFrame
for index, row in stations.iterrows():
    # Extract the station_name and position
    station_name = row['station_name']
    position = row['Position']
    
    # Split the position string to get latitude and longitude
    longitude, latitude = map(float, position.split())
    
    # Store the station_name, latitude, and longitude in the dictionary
    station_coordinates[station_name] = {'latitude': latitude, 'longitude': longitude}

# Define the date range
start_date = '2000-01-01'
end_date = '2020-12-31'

# Function to export images for a specific station
def export_image_for_station(image, station_name,buffered_point):
    # Get the timestamp from system:time_start property
    timestamp = ee.Date(image.get('system:time_start')).format('yyyyMMdd').getInfo()
    
    # Define the folder based on the station name
    folder_name = 'MODIS_LAI_Export/' + station_name
    
    # Export the image to Google Drive
    task = ee.batch.Export.image.toDrive(image=image,
                                         description='MODIS_LAI_' + station_name + '_' + timestamp,
                                         folder=folder_name,
                                         fileNamePrefix='MODIS_LAI_' + station_name + '_' + timestamp,
                                         region=buffered_point.bounds(),
                                         scale=500,
                                         crs='EPSG:4326')
    task.start()

# Iterate over each station in the dictionary
for station_name, coordinates in station_coordinates.items():
    # Extract latitude and longitude for the station
    latitude = coordinates['latitude']
    longitude = coordinates['longitude']
    
    # Define the location (longitude, latitude)
    point = ee.Geometry.Point(longitude, latitude)
    
    # Define a buffer of 500m around the point
    buffered_point = point.buffer(1000)
    
    # Create an image collection for MODIS LAI data
    modis_collection = ee.ImageCollection('MODIS/006/MOD15A2H') \
        .filterBounds(buffered_point) \
        .filterDate(ee.Date(start_date), ee.Date(end_date)) \
        .select(['Lai_500m', 'FparLai_QC', 'LaiStdDev_500m'])  # Add other bands too
    
    # Export all images in the collection for the current station
    image_list = modis_collection.toList(modis_collection.size())
    for i in range(image_list.size().getInfo()):
        export_image_for_station(ee.Image(image_list.get(i)), station_name,buffered_point)
        

