import math
import numpy as np

MONTH_CONTENT = [31,28,31,30,31,30,31,31,30,31,30,31]

def set_rnans(data):
	# Recursive NaN check for any sized array
	for index in range(len(data)):
		try:
			# Abs fails on array
			if abs(data[index]) > 99999:
				data[index] = np.nan
		except:
			# Recursion on each sub-array
			data[index] = set_rnans(data[index])
	return data
			
def simple_mean(point_list):
	# Determine mean from list of points
	# Ignores np.nan values
	sum_points = 0
	sum_count = 0
	for index, value in enumerate(point_list):
		if not np.isnan(value) and value == value and value > -99999 and value < 99999:
			sum_points += value
			sum_count += 1
	if sum_count == 0:
		sum_count = np.nan
	return sum_points/sum_count
	
def recur_mean(point_list):
	# Recursive average for any sized list
	sum_points = 0
	sum_count = 0
	
	for index, value in enumerate(point_list):
		try:
			if not np.isnan(value) and value == value and value > -99999 and value < 99999:
				sum_points += value
				sum_count += 1
		except:
			plen = len(point_list)
			pmean = recur_mean(point_list)
			sum_points += pmean*plen
			sum_count += plen
	fmean = sum_points/sum_count
	return fmean
	
def binning_graph_data(graph_data, nbins, graph_errs = None, do_errs = False, error_lim = None, pop_bins=False, max_mins=None):
	# Number of bins, width of one bin, array of values per bin
	
	# For readability define:
	nvars = len(graph_data)
	npoints = len(graph_data[0])
	
	# Define x properties
	if max_mins == [None,None]:
		largex, smallx = largestsmallest(graph_data[0])
	else:
		largex = max_mins[0][0]
		smallx = max_mins[0][1]
		
	x_range = largex - smallx
	binwidth = x_range/nbins
	# Set arrays 
	bin_array = [[[] for var in range(nvars)] for i in range(nbins)]
	bin_errors = [[[] for var in range(nvars)] for i in range(nbins)]
	bin_values = [[] for var in range(nvars+1)]
	bin_errs = [[] for var in range(nvars)]
	bin_counts = [[] for var in range(nvars)]
	count = 0
	print('Data contains {} points'.format(npoints))
	for index in range(npoints):
		
		
		# Determine bin position for point (by x axis binning)
		try:
			bindex = int((graph_data[0][index] - smallx) / binwidth)
			# Set bindex limits
			if bindex == len(bin_array):
				bindex = len(bin_array)-1
			if bindex == -1:
				bindex = 0
				
			if not (bindex > len(bin_array) or bindex < -1):
				# Calculate xvalue for this bin (always the same for give bindex)
				
				#xvalue = smallx + binwidth*bindex + binwidth * 0.5
				#bin_array[bindex][0].append(xvalue)
				#if do_errs:
				#	bin_errors[bindex][0].append(graph_errs[0][index])
			
				for vdex in range(0, nvars): # Do for each variable except x
				
					bin_array[bindex][vdex].append(graph_data[vdex][index])
					if do_errs:
						bin_errors[bindex][vdex].append(graph_errs[vdex][index])
		except ValueError:
			pass
	# Average each bin
	if pop_bins:
		# do for each bin
		for index, bin_set in enumerate(bin_array):
			for vdex in range(nvars):
				if len(bin_set[vdex]) != 0:
					bin_values[vdex].append( sum(bin_set[vdex])/len(bin_set[vdex]) )
				else:
					bin_values[vdex].append(np.nan)
			bin_values[nvars-1][index] = len(bin_set[vdex])
		return bin_values, [], []
	else:	
		for bindex, bin_set in enumerate(bin_array):
			if bin_set[0] != []:
				bin_values[len(bin_values)-1] = len(bin_set)
				err_vars, means = [], []
			
				for vdex in range(nvars): # Do for each variable
					avg_err = simple_mean(bin_errors[bindex][vdex])
					bin_weights = bin_set[vdex]
					new_bin_weights = []
					if error_lim != None:
						for pointdex in range(len(bin_weights)):
							if bin_errors[bindex][vdex][pointdex] < error_lim * avg_err:
								new_bin_weights.append(bin_weights[pointdex])
					else:
						new_bin_weights = bin_weights
					mean_bin = simple_mean(new_bin_weights)
					bin_values[vdex].append(mean_bin)
				
					# Error in bin values
				
					components = (np.array(new_bin_weights) - mean_bin)**2
					err_vars = math.sqrt( np.sum(components))
					bin_errs[vdex].append(err_vars)
					bin_counts[vdex].append(len(components)) 
		print('Done binning')
		return bin_values, bin_errs, bin_counts
	
def quick_map_to_data(map_bounds, data, abs_bounds, do_overwrite = False):
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

def quick_latlon_to_data(map_bounds, data_bounds, lat, lon):
	abs_lat = lat - map_bounds[0]
	abs_lon = lon - map_bounds[2]
	
	lat_range = map_bounds[1] - map_bounds[0]
	lon_range = map_bounds[3] - map_bounds[2]
	
	data_lat_range = data_bounds[1] - data_bounds[0]
	data_lon_range = data_bounds[3] - data_bounds[2]
	
	data_lat = data_bounds[0] + (abs_lat/lat_range) * data_lat_range 
	data_lon = data_bounds[2] + (abs_lon/lon_range) * data_lon_range 
	
	return data_lat, data_lon
	
def simple_errors(values, errors):
	sum_errs = 0
	for index in range(len(values)):
		value = values[index]
		error = errors[index]
		frac = error/value
		sum_errs += frac**2
	return math.sqrt(sum_errs)
	
def largestsmallest(array):
	largest = -999
	smallest = 999
	for index, item in enumerate(array):
		if item > largest:
			largest = item
		if item < smallest:
			smallest = item
	return largest, smallest
	
def largestsmallest_recur(array):
	try:
		vals = []
		for arr in array:
			lg, sl = largestsmallest_recur(arr)
			vals.append(lg)
			vals.append(sl)
		return largestsmallest_recur(vals)
	except:
		largest = -999
		smallest = 999
		for item in array:
			if abs(item) != 999:
				if item > largest:
					largest = item
				if item < smallest:
					smallest = item
		return largest, smallest
	
def sigma_range(array, sig):
	mean = simple_mean(array)
	sigma = mean_error(mean, array) * math.sqrt(len(array))
	
	large = mean + sigma*sig
	small = mean - sigma*sig
	return large, small
	