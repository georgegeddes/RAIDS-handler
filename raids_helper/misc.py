from numpy import floor
from datetime import datetime

def raids_date(ds):
    """`ds` is a netCDF Dataset from RAIDS."""
    y = ds['YEAR'][:]
    m = ds['MONTH'][:]
    d = ds['DAY'][:]
    dhours = ds['UT_HOUR'][:]
    hours = floor(dhours)
    minutes = floor((dhours-hours)*60)
    seconds = dhours*3600 % 60
    times = zip(hours,minutes,seconds)
    return [datetime(y,m,d,int(H),int(M),int(S)) for (H,M,S) in times]
