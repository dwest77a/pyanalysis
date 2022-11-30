# encoding: utf-8

__author__    = 'Daniel Westwood'
__date__      = '16 Nov 2022'
__copyright__ = 'Copyright 2022 United Kingdom Research and Innovation'
__license__   = 'BSD - see LICENSE file in top-level package directory'
__contact__   = 'daniel.westwood@stfc.ac.uk'

import math
import numpy as np
from pylogger import message, basic

# datasetMath module
# - sigma
# - variance
# - std_error         : standard error in the mean
# - linear_regression
# - science_errors    : correctly formatted err string

def sigma(array):
    """
    Calculate Standard Deviation/Sigma Value
     - Takes array input
     - Calculates standard deviation
    """
	mean = simple_mean(array)
	sig = std_error(mean, array) * math.sqrt(len(array))
	
	return sig
		
def variance(point_list):
    """
    Calculate variance of a set of data
    """
	mean = np.mean(point_list)
	nths = np.array((point_list - mean)**2)
	err = np.sum(nths)
	variance = err/len(point_list)
	return variance
	
def std_error(mean, point_list):
	"""
    Standard Mean Error calculation
    """

    # Calculate error in the mean for values
	point_list = np.array(point_list)
	sum_points = 0
	nths = []
	for pt in point_list:
		nths.append((pt - mean)**2)
	err = np.sum(nths)
        
	n_factor = len(point_list)
	return math.sqrt(err)/n_factor
	
def linear_regression(xvalues, yvalues, VERB=False):
	"""
    Calculate linear regression for a set of x/y values
	 - Line of best fit 
	 - Returns slope and intercept (with errors) json format
    """

    # Function to calculate slope and intercept of linear fit
    if len(xvalues) != len(yvalues):
        print('error: x-y size difference')
        return None
	if VERB:
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
    """
    Determine scientific errors to display
     - Determine appropriate number of sig figs for consistency
	 - Return string with +/- for displaying to graphs
    """

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
   
if __name__ == "__main__":
    basic(__file__)