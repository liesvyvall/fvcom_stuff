from PyFVCOM.read import FileReader
from PyFVCOM.plot import Depth, Plotter
import numpy as np
import matplotlib.pyplot as plt
from cmocean import cm
from PyFVCOM.grid import _grid as grd
from PyFVCOM.grid import line_sample, find_nearest_point, vincenty_distance, haversine_distance
from PyFVCOM.coordinate import lonlat_decimal_from_degminsec
from datetime import datetime
import pandas as pd


def validate_profiles(fvcom_file, in_situ_year, station_number):
    
    # Loading fvcom file
    fvcom = FileReader(fvcom_file, 
                    variables=['time','temp', 'ww', 'h', 'zeta'], zone='12N')

    fvcom.grid.lon = fvcom.grid.lon -360
    fvcom.grid.lonc = fvcom.grid.lonc -360

    # Loading in situ files
    # Creating empty dataframes
    temp_df = pd.DataFrame()
    press_df = pd.DataFrame()
    sal_df = pd.DataFrame()

    for files in np.arange(0, 11):
        # reading single files     
        temp = pd.read_csv('/Users/liesvyvall/Documents/Doctorado/Articulos/2024/'+in_situ_year+'/temperature'+str(files)+".csv", header=None)
        press = pd.read_csv('/Users/liesvyvall/Documents/Doctorado/Articulos/2024/'+in_situ_year+'/pressure'+str(files)+".csv", header=None)
        sal = pd.read_csv('/Users/liesvyvall/Documents/Doctorado/Articulos/2024/'+in_situ_year+'/salinity'+str(files)+".csv", header=None)

        # concatenate data
        temp_df = pd.concat([temp_df, temp], ignore_index=True, axis=1)
        press_df = pd.concat([press_df, press], ignore_index=True, axis=1)
        sal_df = pd.concat([sal_df, sal], ignore_index=True, axis=1)

    lons = pd.read_csv('/Users/liesvyvall/Documents/Doctorado/Articulos/2024/'+in_situ_year+'/longitude.csv', header=None)
    lats = pd.read_csv('/Users/liesvyvall/Documents/Doctorado/Articulos/2024/'+in_situ_year+'/latitude.csv', header=None)
    dates = pd.read_csv('/Users/liesvyvall/Documents/Doctorado/Articulos/2024/2005/dates.csv', header=None)

    temp_array = temp_df.values
    sal_array = sal_df.values
    depth = press_df.values

    lon_array = lons.values.flatten()
    lat_array = lats.values.flatten()

    # Calculate closest node to station position
    #pos_index = fvcom.closest_node((lon_e08[0], lat_e08[0]))
    pos_index = fvcom.closest_node((lon_array[station_number], lat_array[station_number]))

    ## FECHAS
    # Fecha en formato de cadena
    date_str = dates.values[station_number][0]

    # Convertir a datetime y extraer año, mes, día, hora y minuto
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
    result = (date_obj.year, date_obj.month, date_obj.day, date_obj.hour)

    # Calculate closest time to station time
    fecha = datetime(*result)

    # Array of fvcom datetimes
    fvcom_times = fvcom.time.datetime

    # Calculating indice of fvcom closest time to station time
    diffs = np.abs(fvcom_times - fecha)

    # Encontrar el índice de la fecha más cercana
    time_index = np.argmin(diffs)
    
    # Preparing fvcom variables for plot
    profileE08 = fvcom.data.temp[time_index, :, pos_index]

    depth_fvcom = fvcom.grid.siglay_center[:, pos_index]
    lays = fvcom.data.h[pos_index]

    prof = (depth_fvcom*lays)*(-1)

    # Create the figure and axis with higher resolution
    fig, ax = plt.subplots(figsize=(6, 8), dpi=300)  # Increased dpi for better resolution

    # Plot the first temperature profile
    ax.plot(temp_array[:, station_number], depth[:, station_number], label='In-situ Temperature Profile', color='b', linewidth=2)

    # Invert the y-axis
    ax.invert_yaxis()

    # Plot the second temperature profile
    ax.plot(profileE08[0], prof, label='FVCOM Temperature Profile', color='r', linestyle='--', linewidth=2)

    # Set the same depth limits for both profiles
    ax.set_ylim(np.nanmax(depth[:, station_number]), 0)

    # Add labels and title
    ax.set_xlabel('Temperature (°C)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Depth (m)', fontsize=14, fontweight='bold')
    ax.set_title(f"Station at Lon: {lon_array[station_number]:.2f}°, Lat: {lat_array[station_number]:.2f}°\nDate: {date_str[:16]}", fontsize=16, fontweight='bold')

    # Add grid for better readability
    ax.grid(True, linestyle='--', alpha=0.7)

    # Add legend
    ax.legend(fontsize=12)

    # Adjust layout
    plt.tight_layout()

    # Save the figure with a specified resolution
    plt.savefig(f'validation_profile_{station_number}.png', dpi=300)  # Save as PNG with increased dpi


