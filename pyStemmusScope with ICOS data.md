# Running pyStemmusScope with ICOS data


##  About ICOS data.
The Integrated Carbon Observation System (ICOS) provides eddy covariance fluxes at 73 stations within the Europe. 
[The Warm Winter 2020 Ecosystem eddy covariance product ](https://doi.org/10.18160/2G60-ZHAK) was downloaded directly from the website. The eddy covariance fluxes has 73 stations in the ecosystem domain, part of them outside the ICOS network, covering the period 1989-2020. The data are in the standard format used for the ICOS L2 ecosystem products and also used by other regional networks like AmeriFlux. The processing has been done using the ONEFlux processing pipeline (https://github.com/icos-etc/ONEFlux) and is fully compliant and integrable with the FLUXNET2015 release (https://fluxnet.fluxdata.org/) and other datasets processed with the same pipeline (AmeriFlux, ICOS L2).

## Creating forcing data for pyStemmusScope using ICOS station data.
Firstly, the necessary meteorological forcing data for the pyStemmusScope ([Tang,et.al 2024](https://doi.org/10.5194/bg-21-893-2024)) :

The ICOS station data are in the csv format. So, some important steps are needed to convert it into the ALMA format Netcdf files, before they are fed to the pyStemmusScope model. For the pre-processing the forcing data into ALMA format, the same guidelines used by the PLUMBER2 datasets ([Ukkola, et.al 2024](https://doi.org/10.5194/essd-14-449-2022)) were followed. 

This is done in the code conversion_to_ALMA.py. The same naming convention and units were followed. 

The total input data in the ALMA formatted input files are:

Forcings:
| Variables | Source | Where to see|
| ----------- | ----------- |---------- |
| Tair | From ICOS station data| |
| SWdown | From ICOS station data | |
| LWdown | From ICOS station data| |
| VPD | From ICOS station data | |
| Relative Humidity (RH) | If present, from the ICOS station, if not from the formula using (vpd, Tair, pressure) | Check function 'calculate_RH_and_q' |
| Specific Humidity (Qair) |  from the formula using (vpd, Tair, pressure)  | Check function 'calculate_RH_and_q' |
| Pressure (Psurf) | From ICOS station data| |
| Precip | From ICOS station data | |
| Wind | From ICOS station data| |
| CO2air | From ICOS station data, if not available from CAMS dataset| Check function 'get_cams_co2_data' |
| Elevation |From COPERNICUS/DEM/GLO30 |See code getCanopyHeightandElevation.py|
| IGBP land use |If present, from Table C.5.[Prikaziuk, et.al. 2023](https://doi.org/10.1016/j.rse.2022.113324) |
| Height of canopy |If present, from Table C.5.[Prikaziuk, et.al. 2023](https://doi.org/10.1016/j.rse.2022.113324), if not from the ETH_GlobalCanopyHeight_2020_10m_v1   |See code getCanopyHeightandElevation.py|
| Measurement height | If present, from Table C.5. [Prikaziuk, et.al. 2023](https://doi.org/10.1016/j.rse.2022.113324) ||
| Leaf Area Index (LAI) | From MODIS LAI| Described below|


Initial condition:
|Data|Source|Where to see|
| ----------- | ----------- |---------- |
| skin_temperature | From ERA5Land Hourly | |
| soil_temperature_level_1 | From ERA5Land Hourly | |
| soil_temperature_level_2 | From ERA5Land Hourly| |
| soil_temperature_level_3 | From ERA5Land Hourly | |
| soil_temperature_level_4 | From ERA5Land Hourly | |
| volumetric_soil_water_layer_1 | From ERA5Land Hourly | |
| volumetric_soil_water_layer_2 | From ERA5Land Hourly| |
| volumetric_soil_water_layer_3 | From ERA5Land Hourly | |
| volumetric_soil_water_layer_4 | From ERA5Land Hourly | |


**Codes:**

1) **conversion_to_ALMA.ipynb** (This requires all the input information described above and gives ALMA formatted netcdf files in the format pyStemmusScope reads.)
2) get_InitialCondition_ERA5Land_gee.ipynb  (Since the cds requests were processing long time, for mean while initial condition variable for different locations were downloaded from GEE "ECMWF/ERA5_LAND/HOURLY" and written into  "ERA5LandInitialcondition.csv")
3) **prepare_Initialcondition.ipynb** (This reads initial condition data from the "ERA5LandInitialcondition.csv" and produce Initial condition netcdf files for different locations in the format pyStemmusScope reads.)
4) **creating_config_file.ipynb** (This requires information from info_for_configfile.csv and create config file in separate folder as required to run the pyStemmusScope automatically.)
5) **run_model_linux.py** (This runs the pyStemmusScope model in the linux668.)
6) scratch.ipynb (some random analysis)
7) conversion_to_ALMA.py (to run process in the linux terminal)
8) downloadCAMSdataset.py (downloading CAMS data)
9) ERA5LandDataDownload.py (downloading ERA5LandData)
10) ESACCILandCoverDownload.py (downloading landcover data)
11) getCanopyHeightandElevation.py

**Csv files:**

1) ERA5LandInitialcondition.csv --> contains the initial condition variables for different locations.
2) info_for_configfile.csv --> contains information that are needed to autoamtically write the config files for different ICOS stations.
3) sites_with_noNAs.csv --> contains information about which variables have how many missing data points for different ICOS stations.
4) station_with_elevation_heightcanopy.xlsx --> contains elevation and height of canopy (from ETH) as well as measurement height and canopy height collected from the literature.


**LAI processing:**

Steps in the [Ukkola, et.al 2024](https://doi.org/10.5194/essd-14-449-2022) from the section 2.2.5 were followed.  **(See function 'get_LAI' inside 'conversion_to_ALMA.ipynb' or 'conversion_to_ALMA.py'.)**

**Steps to do**
**Preprocessing**
1) Read all csv files containing the LAI information downloaded from the MODIS.
2) Then, select the grid cell containing particular location and neighboring 8 grid cells.
3) Keep only good-quality data (QC flag values0, 2, 24, 26, 32, 34, 56, and 58) and set all other values to missing.
   
**Spatial averaging with weights**

4)  At each time step, calculate a weighted mean from the nine pixels by weighting them by their standard deviation error (defined as $1/\sigma^2$). **(See function 'get_spatial_weighted_LAI')**

**Gap filling**

5)  Gap fill the resulting 8-daily time series using a cubic spline function (Forsythe et al., 1977) and set any negative LAI values set to zero. **(check function 'interpolate_NA_LAI')**
6) Some MODIS time steps were missing in the steps of 8 days, which were filled using the mean of the nearest values. (**check function 'check_data_availability_LAI'**)

**Smoothing** (**check function 'smoothing_LAI'**)

7)  A climatology (46 time steps) was then calculated from all available years.
8)  An anomaly time series was then created by removing the climatology and smoothed by taking a rolling mean over a window of ±6 time steps to further remove short-term variability.
9)  The climatology was then added to the smoothed time series and the 8-daily time series interpolated to the time resolution of
the flux tower data.














