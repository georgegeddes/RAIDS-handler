import netCDF4
import pandas as pd
import os
from glob import glob

from .misc import raids_date

class raids_data_framer( object ):
    def __init__(self,data_dir):
        """Point to the directory where the data was unzipped."""
        self.path = os.path.abspath(data_dir)

    def __str__(self):
        message = "{} pointed to data unzipped to:\n    {}".format
        print(message(self.__class__,self.path))

    def get_spectrum_time_series(self,band,date_range=None,load_raw=False):
        """Load data from .nc files to a pandas Dataframe."""
        # setup
        data_dir = self.path
        band=band.upper()
        filenames = glob(data_dir+'/*/*/*/MUV/*.nc')
        
        # load the ncdf files 
        datasets = [netCDF4.Dataset(fname) for fname in filenames]
        self.ncdf_datasets = datasets
        
        # convert netcdf to pandas data frames
        df_list = []
        for ds in datasets:
            # Start by assembling the spectrum time seriesx and then add more
            dates = pd.DatetimeIndex(raids_date(ds),name='TIMESTAMP')
            df = pd.DataFrame(ds[band+'_INTEN'][:],
                              columns=ds[band+'_WL'],
                              index=dates)

            # list all of the columns that contain non-spectral timestamped data
            ntimes = len(dates)
            timestamped_data_labels = [var for var in ds.variables if ds[var][:].shape==(ntimes,)]

            # # All of this stuff would be cool to have, but this method doesn't work.
            # # copy those values into the data frame
            # housekeeping=pd.DataFrame(index=dates)
            # for var in timestamped_data_labels:
            #     housekeeping[var] = ds[var][:]
            # df.housekeeping=housekeeping

            # # list single data points
            # info = [{var:ds[var][:]} for var in ds.variables if ds[var][:].shape==(1,)]
            # df.other_info = info

            # # attach sensitvity
            # label = band+"_SENS"
            # sensitvity = pd.DataFrame(columns=ds[band+"_WL"])
            # df.sensitvity=sensitvity

            # will we ever need the raw data? probably not
            if load_raw:
                raise NotImplementedError("This hasn't been coded yet") 
                # label = band+"_"+raw
                # df[label] = ds[label][:]           

            df_list.append(df.copy())
        data = pd.concat(df_list)

        # return the whole thing or just a chunk        
        if date_range:
            return data[date_range]
        else:
            return data
