import sympy as sp
from dtumathtools import *
sp.init_printing()
from sympy.solvers.solveset import linsolve
import math as math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



fname_2290 = r'/Users/Raphael/Documents/GitHub_repositories/Hydrology-group-8/hydrology-group-8/Assignment_2/Assignment_2_data/produkt_pkt_aero_20210101_20211229_02290.txt'
fname_4466 = r'/Users/Raphael/Documents/GitHub_repositories/Hydrology-group-8/hydrology-group-8/Assignment_2/Assignment_2_data/produkt_pkt_aero_20210101_20211231_04466.txt'

data_2290 = pd.read_csv(fname_2290,delimiter = ';')
data_4466 = pd.read_csv(fname_4466,delimiter = ';')

data_2290 = data_2290.replace(-999,np.nan)
data_4466 = data_4466.replace(-999,np.nan)


date = 2021010406
day_data_2290 = data_2290.loc[data_2290['MESS_DATUM'] == date]
date = 2021010400
day_data_4466 = data_4466.loc[data_4466['MESS_DATUM'] == date]





# redefining all the previous code not for one day anymore but for data of the whole year
Rda = 287 # [JKG^-1K^-1]

all_air_pressure2290 = data_2290['AEP'].to_numpy()
all_air_pressure4466 = data_4466['AEP'].to_numpy()

all_T2290 = data_2290['AET'].to_numpy()
all_T4466 = data_4466['AET'].to_numpy()

all_water_vapour_pressure2290 = 611 * 10 ** ((7.5 * (all_T2290)) / (all_T2290 +273.15 - 35.85))
all_water_vapour_pressure4466 = 611 * 10 ** ((7.5 * (all_T4466)) / (all_T4466 +273.15 - 35.85))

all_water_vapour_density2290 = (0.622 * all_water_vapour_pressure2290) / (Rda * (all_T2290+273.15))
all_water_vapour_density4466 = (0.622 * all_water_vapour_pressure4466) / (Rda * (all_T4466+273.15))

all_mixing_ratio2290 = (0.622*all_water_vapour_pressure2290) / all_air_pressure2290
all_mixing_ratio4466 = (0.622*all_water_vapour_pressure4466) / all_air_pressure4466

all_dry_air_density2290 = all_water_vapour_density2290/all_mixing_ratio2290
all_dry_air_density4466 = all_water_vapour_density4466/all_mixing_ratio4466

all_moist_air_density2290 = all_dry_air_density2290 + all_water_vapour_density2290
all_moist_air_density4466 = all_dry_air_density4466 + all_water_vapour_density4466

all_specific_humidity2290 = all_water_vapour_density2290/all_moist_air_density2290
all_specific_humidity4466 = all_water_vapour_density4466/all_moist_air_density4466




import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Not strictly needed in newer matplotlib, but sometimes good to keep


# ------------------------------------------------------------------------------
# 1. Read / prepare your data
# ------------------------------------------------------------------------------
# Example: Suppose you have a DataFrame called data_2290 from your CSV
# Make sure each column you need is in numeric form (floats, ints, or properly converted).
# If needed, parse 'MESS_DATUM' as numeric or ordinal. Otherwise, you can keep it as datetime 
# and convert to, e.g., a timestamp integer for the Y-axis.

# Example for time axis:
# data_2290['MESS_DATUM'] = pd.to_datetime(data_2290['MESS_DATUM'], format='%Y%m%d%H')
# data_2290['time_ordinal'] = data_2290['MESS_DATUM'].map(pd.Timestamp.toordinal)
# or simply use the numeric values in MESS_DATUM if they’re already in yyyymmddhh format

time_axis = data_2290['MESS_DATUM'].to_numpy()  # or data_2290['time_ordinal'].to_numpy()
geopotential_elevation = data_2290['AEH'].to_numpy()

# ------------------------------------------------------------------------------
# 2. Create a 3D scatter plot
# ------------------------------------------------------------------------------
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# You can color the points by another variable if you like:
sc = ax.scatter(
    all_specific_humidity2290,   # X
    time_axis,                   # Y
    geopotential_elevation,      # Z
    c=geopotential_elevation,    # color by AEH, or something else
    cmap='viridis',
    marker='o',
    s=10,                        # marker size
    alpha=0.7                    # transparency (optional)
)

# Add colorbar (optional)
cbar = plt.colorbar(sc, ax=ax, pad=0.1)
cbar.set_label('Geopotential Elevation (AEH)', rotation=270, labelpad=15)

# ------------------------------------------------------------------------------
# 3. Label axes and show
# ------------------------------------------------------------------------------
ax.set_xlabel('Specific Humidity')
ax.set_ylabel('Time Steps (MESS_DATUM)')  # or 'time_ordinal' if you used that
ax.set_zlabel('Geopotential Elevation (AEH)')

plt.title('3D Scatter: Specific Humidity vs Time vs Geopotential Elevation')
plt.tight_layout()
plt.show()
