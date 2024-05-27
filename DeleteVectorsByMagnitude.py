# %%
from PyFVCOM.current import scalar2vector, vector2scalar
import numpy as np

def delete_vectors(u_velocity, v_velocity, critical_value):
    dir, mag = vector2scalar(u_velocity, v_velocity)

    mag_2=mag

    for t in range(0, len(u_velocity[:, 0])):   
        indice_mag = np.argwhere((mag[t, :] >= critical_value))
        mag_2[t, indice_mag] =0.001

    u_modified, v_modified = scalar2vector(dir, mag_2)

    return u_modified, v_modified




