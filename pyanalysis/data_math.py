# encoding: utf-8

__author__ = 'Daniel Westwood'
__date__ = '16 Nov 2022'
__copyright__ = 'Copyright 2022 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'daniel.westwood@stfc.ac.uk'

import math
import numpy as np
from pylogger import message, basic

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
	
def variance(mean, point_list):
	sum_points = 0
	nths = np.array((point_list - mean)**2)
	err = np.sum(nths)
	variance = err/len(point_list)
	return variance
	
def mean_error(mean, point_list):
    # Calculate error in the mean for values
	point_list = np.array(point_list)
	sum_points = 0
	nths = []
	for pt in point_list:
		nths.append((pt - mean)**2)
	err = np.sum(nths)
        
	n_factor = len(point_list)
	return math.sqrt(err)/n_factor
	
def np_linear_regressions(xvalue_array, yvalue_array):
	if xvalue_array.size != yvalue.size:
		print('Error: X-Y size difference')
		return None
	xmeans = np.nanmean(xvalue_array, axis=0)
	ymeans = np.nanmean(yvalue_array, axis=0)
	
	#x_std_errs = np.nanstd(xvalue_array, axis=0) / math.sqrt(len(xvalue_array))
	#y_std_errs = np.nanstd(yvalue_array, axis=0) / math.sqrt(len(yvalue_array))
	
	#frac_errs = np.sqrt(3*np.square(x_std_errs/xmeans) + np.square(y_std_errs/ymeans)
	
	x_xmeans = xvalue_array - np.reshape(np.repeat(xmeans, len(xvalue_array)), (len(xvalue_array), len(xvalue_array[0]), len(xvalue_array[0][0])))
	y_ymeans = yvalue_array - np.reshape(np.repeat(ymeans, len(yvalue_array)), (len(yvalue_array), len(yvalue_array[0]), len(yvalue_array[0][0])))
	
	covariances = np.nansum(x_xmeans*y_ymeans, axis=0)/len(xvalue_array)
	variances = np.nansum(np.square(x_xmeans), axis=0)/len(xvalue_array)
	
	slopes = covariances/variances
	#intercepts = ymeans - slope*xmeans
	
	#slope_errs = slopes*frac_errs
	#intercept_errs = intercepts*frac_errs
	
	return slopes
	   
def linear_regression(xvalues, yvalues):
    # Function to calculate slope and intercept of linear fit
    if len(xvalues) != len(yvalues):
        print('error: x-y size difference')
        return None
    print('XVALUES',xvalues)
    print('YVALUES',yvalues)
    # Calculate means of xvalues and yvalues
    xmean = simple_mean(xvalues)
    ymean = simple_mean(yvalues)
    
    # Covariance = sum [ (xvalue - xmean)*(yvalue - ymean) ] 
    # Covariances - array of all components 
    # Variance = sum [ (xvalue - xmean)**2 ]
    # Variances - array of all components
    
    x_std_err = mean_error(xmean, xvalues)
    y_std_err = mean_error(ymean, yvalues)
    
    frac_err = math.sqrt( 3*(x_std_err/xmean)**2 + (y_std_err/ymean)**2 )
    
    covariance, variance = 0, 0
    covariances, variances = [], []
    for index in range(len(xvalues)):
        xval = xvalues[index]
        yval = yvalues[index]
        if not np.isnan(xval) and not np.isnan(yval):
            x_xmean = xvalues[index] - xmean
            y_ymean = yvalues[index] - ymean
        
            covariance += x_xmean*y_ymean
            covariances.append(x_xmean*y_ymean)
            variance += x_xmean**2
            
            variances.append(x_xmean**2)
    # Error correction
    covariance = covariance/len(xvalues)
    variance = variance/len(xvalues)
    # zero variance means all values are zero
    if variance != 0:
		
        slope = covariance/variance
        intercept = ymean - slope*xmean
		
        slope_err = slope*frac_err
        intercept_err = intercept*frac_err
		
        return {'slope':[slope, slope_err],'intercept':[intercept,intercept_err]}
    else:
        return None
	
def science_errors(value,err):
    # Write value/error pair with same number of sig. figs. defined by error range
    value_sign = value/abs(value)
    # Take absolute values for ease of digits
    err = abs(err)
    value = abs(value)
    strerr = '{0:.15f}'.format(err)
    strval = '{0:.15f}'.format(value)
    
    decim_index = len(strerr)
    dig_index = 0
    is_decim, is_digit = False, False
    # Determine which index in strerr is a . and which is a non-zero digit
    for index, digit in enumerate(strerr):
        if digit == '.' and is_decim == False:
            decim_index = index
            is_decim = True
        if digit != '.' and digit != '0' and is_digit == False:
            dig_index = index
            is_digit = True
    # If error > 1
    if decim_index > dig_index:
        # Format value and err to same number of digits
        dps = str(format(decim_index-1,'02d')) + 'd'
        valuestr = str(round(value,-(decim_index-1)))
        errstr = format(int(round(err)),dps)
    else:
        # Format now applies to floating point numbers
        dps = str(dig_index-decim_index)
        valuestr = format(round(value,dig_index-decim_index),'.'+dps+'f')
        errstr = format(err,'.'+dps+'f')
    # Add sign back to value string
    if value_sign < 0:
        valuestr = '-' + valuestr
        
    return valuestr+u"\u00B1"+errstr # Return with +-	
 
def date_to_value(day,month,year):
	# Calculate number of days since day zero
	# Zero Day defined as 01/01/1994 (Earlier than all instruments)
	# return value - number ofdays
	
	days_so_far = (float(day) - 1.0)
	for month in range(int(month) - 1):
		if month > 11:
			month -= 12
			days_so_far += 365
		days_so_far += MONTH_CONTENT[month]
		
	days_so_far += 365*(int(year) - 1994)
	return days_so_far
   
if __name__ == "__main__":
    basic(__file__)