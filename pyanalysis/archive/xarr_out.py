import xarray as xr
import matplotlib.pyplot as plt

import cartopy.crs as ccrs

MAP_AX_D = [0.05,0.5,0.9,0.45]

def configure_map_coords(map_bounds, ctype):
    if ctype == 'gmed': # Greenwich Medium
        pass
    elif ctype == 'amed': # Asian Medium
        if map_bounds[2] < 0:
            map_bounds[2] = map_bounds[2] + 360
        if map_bounds[3] < 0:
            map_bounds[3] = map_bounds[3] + 360
    else:
        print('XOutError: Unrecognised ctype in configure_map_coords: {}'.format(ctype))
        pass
    return map_bounds

def cut_by_region(variable, map_bounds,drop=True,ctype='gmed'): # LLS required
    map_bounds = configure_map_coords(map_bounds, ctype)
    lats = variable.lat
    lons = variable.lon
    var = variable.where( (lats>map_bounds[0]) & (lats<map_bounds[1]) & (lons>map_bounds[2]) & (lons<map_bounds[3]),drop=drop)
    return var

def simple_plot(fig, variable, map_axes=MAP_AX_D,projection=None,map_title='Map Title'):
    map_ax = fig.add_axes(map_axes, projection=projection)

    splot = variable.plot(ax=map_ax)
    if projection != None:
        splot.axes.coastlines()
    splot.axes.set_title(map_title)
    return fig

def lls_open_dataset(filename):
    data = xr.open_dataset(filename)
    find, replace = [], []
    latitudes = ['Lat','Latitude','latitude']
    longitudes = ['Lon','Longitude','longitude']

    for d in data.variables:
        if d in latitudes and d != 'lat':
            find.append(d)
            replace.append('lat')
        if d in longitudes and d != 'lon':
            find.append(d)
            replace.append('lon')
    if len(find) != 0:
        dict = {}
        for x in range(len(find)):
            dict[find[x]] = replace[x]
        return data.rename(dict)
    else:
        return data

if __name__ == "__main__":
    print('pyanalysis: xarr_out.py')

    badc = '/badc/ecmwf-era-interim/data/gg/as/2010/01/01/ggas201001010000.nc'
    c3s = '/gws/nopw/j04/cds_c3s_cloud/public/c3s_312b_lot1/data/srb/esa_cci/tcdr/r01/monthly/2001/01/C3S-312bL1-L3C-MONTHLY-SRB-ATSR2_ORAC_ERS2_200101_fv3.0.nc'

    badc_var = 'T2'
    c3s_var = 'srb'

    inp_switch = 'c3s'

    if inp_switch == 'c3s':
        ctype = 'gmed'
        data = lls_open_dataset(c3s)
        var = data[c3s_var]
    else:
        ctype = 'amed'
        data = lls_open_dataset(badc)
        var = data[badc_var]

    fig = plt.figure()
    sam_bounds = [-51.8, 16.8, -83.2, -17.7]
    var_sam = cut_by_region(var, sam_bounds, ctype=ctype)
    fig = simple_plot(fig, var_sam, projection=ccrs.PlateCarree())
    plt.show()