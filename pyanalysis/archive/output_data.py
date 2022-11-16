
##            DW Standard Python Library

##   Solutions for graphing data and performing outputs

# Daniel Westwood (daniel.westwood@stfc.ac.uk)

# Updates:
#   - Added to standard python library (14/05/2021)

# ---------------- output_data.py --------------------

## NetCDF4
from netCDF4 import Dataset

## Matplotlib Packages
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Path, PathPatch
from matplotlib import colors
import matplotlib.widgets as wg
import matplotlib as m
import matplotlib.ticker as ticker
m.use('TkAgg') ## Faster rendering

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.path as Path

## System
import os
import sys
from datetime import datetime
from getopt import getopt

## Numpy
import numpy as np
import numpy.ma as ma
import math

map_ax_d = [0.05,0.5,0.9,0.45]
cbar_ax_d = [0.25,0.47,0.5,0.02]
graph_ax_d = [0.1,0.5,0.8,0.45]
gform_d = 'Straight'
map_t_d = 'Map Title'
cbar_t_d = 'Colourbar Title'
graph_t_d = 'Graph Title'
	
def find_lats(ncf):
	lat_dims = ['lat','latitude']
	return find_dims(ncf, lat_dims)

def find_lons(ncf):
	lon_dims = ['lon','longitude']
	return find_dims(ncf, lon_dims)

def find_dims(ncf, dims):
	var_id = ''
	for dim in dims:
		for var in ncf.variables:
			if var == dim:
				var_id = var
	return var_id

def simple_plot(figure, filename, variable, spc=None, scale=1, offset=0,
                map_axes=map_ax_d, cbar_axes=cbar_ax_d, map_title=map_t_d, cbar_title=cbar_t_d,
                color='viridis', alpha=0.7, landsea = 'land+sea', map_bounds=None, value_bounds=None):
	# Import data
	try:
		ncf = Dataset(filename, 'r', format='NETCDF4')
	except:
		print('Failed to load ',filename)
		return None
	
	latlist = ncf[find_lats(ncf)]
	lonlist = ncf[find_lons(ncf)]
	if map_bounds == None:
		map_bounds = [np.float32(latlist[0]), np.float32(latlist[len(latlist)-1]),
					  np.float32(lonlist[0]), np.float32(lonlist[len(lonlist)-1])]
	res = latlist[1] - latlist[0]
	if spc != None:
		dt = ncf[variable][spc]
	else:
		dt = ncf[variable]
	data = np.array(dt)*scale + offset
	#data[data > 150] = np.nan
	data = pm.set_rnans(data)
	data_bounds = [0, len(data), 0, len(data[0])]
	if value_bounds == None:
		large, small = pm.largestsmallest_recur(data)
		value_bounds = [small, large, 0, 0]
	#value_bounds = [270, 320, 0, 0]
	print('Creating Map')
	figure = output_map(figure, data,
	                    map_bounds, res, data_bounds, value_bounds,
	                    map_axes, cbar_axes, map_title, cbar_title,
                        color, alpha, landsea)
	
				
	# Determine Map Bounds
	# Determine Resolution
	# Determine Data Bounds
	# Determine Value Bounds
	
	return figure

def output_map(figure, data, 
               map_bounds, res, data_bounds, value_bounds, # Mandatory fields
               map_axes=map_ax_d, cbar_axes=cbar_ax_d, map_title=map_t_d, cbar_title=cbar_t_d,
               color='viridis', alpha=0.7, landsea = 'land+sea', labsize=10):
		   
	# Create map figure and manage graph output figure given precalculated data
	# Manages png exporting
	# Figure layout set by out_form dictionary
	## Data dimensions checking
	map_ax = figure.add_axes(map_axes)
	map_ax.set_title(map_title)
	ecv_map = Basemap(projection='cyl',llcrnrlat=map_bounds[0], urcrnrlat=map_bounds[1], llcrnrlon=map_bounds[2], urcrnrlon=map_bounds[3], lat_ts=20, resolution='l')

	# Coastlines and countries 
	ecv_map.drawcoastlines()
	ecv_map.drawcountries()
	ecv_map.drawparallels(np.arange(-90.,91.,30.))
	ecv_map.drawmeridians(np.arange(-180.,181.,60.))
	ecv_map.drawmapboundary(fill_color='grey')
		
	data_len = data_bounds[1] - data_bounds[0]
	data_wid = data_bounds[3] - data_bounds[2]
	try:
		if len(data) != data_len or len(data[0]) != data_wid:
			print('DimensionError: Inconsistent Data Dimensions')
	except:
		print('DataError: Expected data set is empty')
		
	latlist, lonlist = [], []
	
	# Create Lat/Lon grid
	lat = map_bounds[0] # Single grid square offset
	lcount = data_bounds[0]
	while lcount < data_bounds[1]:
		latlist.append(lat)
		lat += res
		lcount += 1
	
	lon = map_bounds[2]
	lcount = data_bounds[2]
	while lcount < data_bounds[3]: # Double grid square offset?
		lonlist.append(lon)
		lon += res
		lcount += 1
		
	lon2d,lat2d = np.meshgrid(lonlist, latlist)
	grid_x,grid_y = ecv_map(lon2d,lat2d)
	#ecv_map_color = ecv_map.pcolor(grid_x,grid_y,np.ma.masked_where(np.isnan(data),data), cmap = color, alpha=float(alpha))
	ecv_map_color = ecv_map.pcolor(grid_x,grid_y,data, cmap = color, alpha=float(alpha))
	if landsea != 'land+sea':
		# Block sea
		x, y = ecv_map(lonlist, latlist)
	
		x0, x1 = map_ax.get_xlim()
		y0, y1 = map_ax.get_ylim()
		map_edges = np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]])
	
		polys = [p.boundary for p in ecv_map.landpolygons]
		if landsea == 'land':
			polys = [map_edges]+polys[:]
		else: # sea
			polys = polys[:]
		
		codes = [[Path.MOVETO] + [Path.LINETO for p in p[1:]] for p in polys]
		
		polys_lin = [v for p in polys for v in p]
		codes_lin = [c for cs in codes for c in cs]
		
		path = Path(polys_lin, codes_lin)
		patch = PathPatch(path, facecolor='white',lw=0)
		
		map_ax.add_patch(patch)
			
	## Color Bar Definition
		
	tick_at = []
	for i in range(0,5):
		tick_at.append(value_bounds[0] + i*(value_bounds[1] - value_bounds[0])/5)
	tick_at.append(value_bounds[1])
		
	def fmt(x, pos):
		a, b = '{:.2e}'.format(x).split('e')
		b = int(b)
		return '{}e{}'.format(a, b)

	colorbar_ax = figure.add_axes(cbar_axes)
	colorbar = plt.colorbar( ecv_map_color, cax = colorbar_ax, orientation = 'horizontal', extend='both', ticks = tick_at)#, format=ticker.FuncFormatter(fmt))
	colorbar.ax.tick_params(labelsize=labsize)
		
	## Set colourbar limits depending on value constraints (triangles and lines for limits)
	min_lim = value_bounds[0]
	max_lim = value_bounds[1]
	in_min_lim = float(value_bounds[2])
	in_max_lim = float(value_bounds[3])

	plt.clim(min_lim,max_lim)
	if in_min_lim != in_max_lim:
		colorbar.ax.plot(in_min_lim,-2,'r|',color='black')
		colorbar.ax.plot(in_min_lim,1,'r|',color='black')
		colorbar.ax.plot(in_max_lim,-1,'r|',color='black')
		colorbar.ax.plot(in_max_lim,2,'r|',color='black')
	colorbar.ax.set_xlabel(cbar_title, verticalalignment='center', horizontalalignment='center')
	
	return figure
	
def output_time_series(figure, time_array, graph_data, graph_errs, 
                       graph_title=graph_t_d,
                       graph_axes=graph_ax_d, graphformat=gform_d,
                       do_errs=False, ylabel=''):
	# Output graph below map onto main output figure
	# Create graph title based on location constraints used
	# tick labels limited so not too dense labelling   
	# Create graph ax (subplot)   
	graph_ax = figure.add_axes(graph_axes)
	
	# Define y label strings

	# Set labels to graph
	graph_ax.set_ylabel(ylabel)
	graph_ax.set_xlabel('Time')
	
	graph_ax.set_title(graph_title)
		
	graph_labels = []
	graph_ticks = []
	# Determine ticks and labels for x axis (time)
	print(graph_data)
	tick_factor = int(1 + len(graph_data[0])/5)
	for index in range(len(graph_data[0])):
		
		if (index+1)%tick_factor != 0:
			graph_labels.append('')
		else:
			if graphformat == 'Straight':
				graph_labels.append(time_array[index])
			elif graphformat == 'Loop':
				graph_labels.append(time_array[index])
			else:
				print(graphformat)
				
		graph_ticks.append(index+1)
	graph_ax.set_xticks(graph_ticks)
	#if len(graph_labels) < 5:
	graph_ax.set_xticklabels(graph_labels, rotation='horizontal')
	#else:
	#	graph_ax.set_xticklabels(graph_labels, rotation='vertical')
	
	#plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)  
	# Extend limits below and above for space at edge of graph
	graph_ax.set_xlim([0, len(graph_labels)+1])
	if do_errs:
		# Graph with error bars
		m.rcParams.update({'errorbar.capsize':5})
		for var_index in range(len(graph_data)):
			print(graph_ticks, graph_data[var_index], graph_errs[var_index])
			graph_ax.errorbar(graph_ticks, graph_data[var_index], 
							  yerr=graph_errs[var_index], capsize=5)
	else:
		for var_index in range(1, len(graph_data)):
			graph_ax.plot(graph_ticks, graph_data[var_index])
			
	return figure
	
def output_two_var_graph(figure, graph_data, graph_errs=None, 
                         graph_title=graph_t_d,
                         graph_axes=graph_ax_d,
                         do_errs=False, do_bins=False, do_reg=True, 
                         nbins=20, xlabel='', ylabel='', error_lim=None, 
                         graph_lims=None, str_lines=None, do_hist=False,
                         max_mins=[None,None]):
	# Output graph below map onto main output figure
	# Create graph title based on location constraints used
	# tick labels limited so not too dense labelling   
		
	# Create graph ax (subplot)   
	graph_ax = figure.add_axes(graph_axes)
	print('Setup Graph')
	graph_ax.set_ylabel(ylabel) 
	graph_ax.set_xlabel(xlabel)
	graph_ax.set_title(graph_title)
		
	maxes, mins, ranges, lims = [], [], [], []
	for index in range(2): # Plot two variables
		if max_mins[index] == None:
			large, small = pm.largestsmallest(graph_data[index])
		else:
			large = max_mins[index][1]
			small = max_mins[index][0]
		maxes.append(large)
		mins.append(small)
		ranges.append(large-small)
		lims.append([ small - (large-small)*0.2, large + (large-small)*0.2])
	if graph_lims == None:
		graph_ax.set_ylim(lims[1])
		graph_ax.set_xlim(lims[0])
	else:
		graph_ax.set_ylim(graph_lims[1])
		graph_ax.set_xlim(graph_lims[0])
		
	# Scale factors for text writing
	xscale = ranges[0]/10
	yscale = ranges[1]/10
		
		
	if not do_bins:
		xvalues, yvalues = [], []
		xvalue_errs, yvalue_errs = [], []
		# Assemble x-y data and errors in correct format
		for index in range(len(graph_data[0])):
			if not np.isnan(graph_data[0][index]) and not np.isnan(graph_data[1][index]):
				xvalues.append(graph_data[0][index])
				yvalues.append(graph_data[1][index])
				if do_errs:
					xvalue_errs.append(graph_errs[0][index])
					yvalue_errs.append(graph_errs[1][index])
	else:
		# Get data arrays from external function
		print('Binning Data')
		bin_values, bin_errs, bin_counts = pm.binning_graph_data(graph_data, nbins, graph_errs=graph_errs, do_errs=do_errs, error_lim=error_lim, pop_bins=do_hist, max_mins=max_mins)
		xvalues = bin_values[0]
		yvalues = bin_values[1]
		print(xvalues, yvalues)
		if do_errs:
			xvalue_errs = np.array(bin_errs[0]) / np.array(bin_counts[0])
			yvalue_errs = np.array(bin_errs[1]) / np.array(bin_counts[1])
			
			xvalue_stds = np.array(bin_errs[0]) / np.sqrt(np.array(bin_counts[0]))
			yvalue_stds = np.array(bin_errs[1]) / np.sqrt(np.array(bin_counts[1]))
	
	# Line of best fit for comparison
	if do_reg:
		mc = pm.linear_regression(xvalues, yvalues)
		slope = mc['slope'][0]
		slope_err = mc['slope'][1]
		icept = mc['intercept'][0]
		icept_err = mc['intercept'][1]
	
		# Plot line of best fit labels
		if slope >= 0:
			xlabelloc = ((8.5*xscale) + lims[0][0])
			ylabellocA = ((3*yscale) + lims[1][0])
			ylabellocB = ((0.5*yscale) + lims[1][0])
		elif slope < 0:
			xlabelloc = ((8.5*xscale) + lims[0][0])
			ylabellocA = ((10*yscale) + lims[1][0])
			ylabellocB = ((8.5*yscale) + lims[1][0])
		
		graph_ax.text(xlabelloc, ylabellocA,
					'Slope={}'.format(pm.science_errors(slope,slope_err)),
					style='normal',
					bbox={'facecolor':'white','alpha':0.5,'pad':5})
				  
		graph_ax.text(xlabelloc, ylabellocB,
					'Intercept={}'.format(pm.science_errors(icept, icept_err)),
					style='normal',
					bbox={'facecolor':'white','alpha':0.5,'pad':5})			 
				  
		graph_ax.legend(loc='upper left')
		# y = mx+c - line of best fit plotting
		xpoint1 = lims[0][1] # Max
		xpoint2 = lims[0][0] # Min
	
		ypoint1 = slope*xpoint1 + icept
		ypoint2 = slope*xpoint2 + icept
	
		graph_ax.plot([xpoint1, xpoint2],[ypoint1,ypoint2])
		
	if str_lines != None:
		for line in str_lines:
			xchange = line[0]
			ychange = line[1]
			graph_ax.plot(xchange, ychange)
	
	if do_errs:
		# Standard Error (in the mean)
		if len(xvalue_errs) > 0:
			graph_ax.errorbar(xvalues, yvalues, 
							  xerr=xvalue_errs, yerr=yvalue_errs, 
							  fmt="go", label='std err', capsize=3, capthick=1)
			graph_ax.legend(loc='upper left')
		# Standard Deviation
		if do_bins:
			if len(xvalue_stds) > 0:
				graph_ax.errorbar(xvalues, yvalues,
								xerr = xvalue_stds, yerr=yvalue_stds,
								fmt="ro", label='std dev', capsize=3, capthick=1)
				graph_ax.legend(loc='upper left')
	else:
		graph_ax.scatter(xvalues, yvalues)
		
	return figure
