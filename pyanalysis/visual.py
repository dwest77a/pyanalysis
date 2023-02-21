# encoding: utf-8

__author__    = 'Daniel Westwood'
__date__      = '16 Nov 2022'
__copyright__ = 'Copyright 2022 United Kingdom Research and Innovation'
__license__   = 'BSD - see LICENSE file in top-level package directory'
__contact__   = 'daniel.westwood@stfc.ac.uk'

from pyanalysis.pylogger import message, basic

def sliceMap(map_bounds, data, abs_bounds, do_overwrite = False):
	# Convert map bounds to bounds relative to the data
	# Abs bounds is the range of the data as it is
	# Map bounds is the range to be applied using data bounds
	
	lat_range = abs_bounds[1] - abs_bounds[0]
	lon_range = abs_bounds[3] - abs_bounds[2]
	
	data_len = len(data)
	data_wid = len(data[0])
	
	data_bounds = [0,0,0,0]
	data_bounds[0] = int((map_bounds[0] - abs_bounds[0]) * (data_len/lat_range))
	data_bounds[1] = int((map_bounds[1] - abs_bounds[0]) * (data_len/lat_range))
	data_bounds[2] = int((map_bounds[2] - abs_bounds[2]) * (data_wid/lon_range))
	data_bounds[3] = int((map_bounds[3] - abs_bounds[2]) * (data_wid/lon_range))
	
	if do_overwrite:
		new_data = []
	
		# Reshape data array to new constraints
		for d_index in range(data_bounds[0], data_bounds[1]):
			new_row = []
			for r_index in range(data_bounds[2], data_bounds[3]):
				new_row.append(data[d_index][r_index])
			new_data.append(new_row)
	
		return new_data	
	else:
		return data_bounds

def convertCoords(map_bounds, data_bounds, lat, lon):

	data_lat = convertCoord(map_bounds[0:2], data_bounds[0:2], lat)
	data_lon = convertCoord(map_bounds[2:4], data_bounds[2:4], lon)
	
	return data_lat, data_lon

def convertCoord(spatial, data, coord):
    abs_coord     = coord - spatial[0]
    spatial_range = spatial[1] - spatial[0]

    data_range    = data[1] - data[0]
    data_coord    = data[0] + abs_coord * (data_range/spatial_range)
    
    return data_coord

if __name__ == "__main__":
    basic(__file__)