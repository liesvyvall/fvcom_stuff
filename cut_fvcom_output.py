# %%
# Cut by latitude and longitude coordinates a FVCOM model output 
from PyFVCOM.read import FileReader
import numpy as np

# %%
# %% file load
def cut_fvcom(min_lon, max_lon, min_lat, max_lat, file_name, variables):

    fvcom_data = FileReader(file_name, variables=['latc', 'lonc'])

    if (fvcom_data.data.lonc > 180).any():
        indices = np.argwhere((fvcom_data.data.latc >= min_lat) & (fvcom_data.data.latc <= max_lat) & 
                            (fvcom_data.data.lonc <= (max_lon+360)) & (fvcom_data.data.lonc >= (min_lon+360)))

    else:
        indices = np.argwhere((fvcom_data.data.latc >= min_lat) & (fvcom_data.data.latc <= max_lat) & 
                            (fvcom_data.data.lonc <= (max_lon)) & (fvcom_data.data.lonc >= (min_lon)))


    indices_list = indices.tolist()
    indices_sq = np.squeeze(indices_list)
    #%% read
    fvcom_data = FileReader(file_name,
                        dims={'nele': indices_sq},
                        variables=variables)
    return fvcom_data

# %%



