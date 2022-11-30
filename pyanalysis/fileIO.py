# encoding: utf-8

__author__    = 'Daniel Westwood'
__date__      = '16 Nov 2022'
__copyright__ = 'Copyright 2022 United Kingdom Research and Innovation'
__license__   = 'BSD - see LICENSE file in top-level package directory'
__contact__   = 'daniel.westwood@stfc.ac.uk'

import re
import os
import sys
import glob

from pylogger import basic

def count_files(master_dir, starts, ends, incl=''):
	file_count = 0
	for root, dirnames, filenames in os.walk(master_dir, followlinks=True):
		for filename in filenames:
			if filename.startswith(starts) and filename.endswith(ends):
				if type(incl) == list and incl != []:
					is_all = True
					for inc in incl:
						if inc != '' and inc not in filename:
							is_all = False
					if is_all:
						file_count += 1
				elif incl == '' or (incl != '' and type(incl) == str and incl in filename):
					file_count += 1
	return file_count
    
def get_files(master_dir, starts, ends, incl=''):
	files_dict = {}
	for root, dirnames, filenames in os.walk(master_dir, followlinks=True):
		for filename in filenames:
			if filename.startswith(starts) and filename.endswith(ends):
				if incl == '' or (incl != '' and incl in filename):
					files_dict[filename] = root + '/' + filename
			else:
				print(filename, starts, ends)
	return files_dict
    
def list_files(master_dir, starts='', ends='', incl=''):
	files_arr = []
	for root, dirnames, filenames in os.walk(master_dir, followlinks=True):
		for filename in filenames:
			if (starts == '' or filename.startswith(starts)) and (ends == '' or filename.endswith(ends)):
				if type(incl) == list and incl != []:
					is_all = True
					for inc in incl:
						if inc != '' and inc not in filename:
							is_all = False
					if is_all:
						files_arr.append(root + '/' + filename)
				elif incl == '' or (incl != '' and incl in filename):
					files_arr.append(root + '/' + filename)
	return files_arr
    
def get_from_file(filepath, filename, filetype):
	# General Function for reading from a file (.con format)
	# Used to obtain Plot config info, config dictionaries etc.
	# Outputs a dictionary of input values
	# config (.con) Line Format ---- %key:value%

    try:
        file_contents = open('{}{}'.format(filepath + filename, filetype) ,'r')
    except:
        print('{} file not found ({} type)'.format(filename,filetype))
        return None
    in_data = file_contents.readlines()
    out_dict = {}
    # Line carry over, key and value variables
    carry_over, on_key, on_value = False, False, False
    key, value = '',''
    # Multiple values in array
    value_array = []
    
    for line in in_data:
		# Reset for each new line
        if not carry_over:
            on_key, on_value = False, False
            key, value = '',''
            value_array = []
        else:
            carry_over = False
        # Ignore commented lines
        if line[0] != '#':
            for char in line:
                if char == '&':
                    carry_over = True
                if char == '%' and on_value == False:
                    on_key = True
                if char == '%' and on_value == True:
                    on_value = False
                    if len(value_array) != 0:
                        value_array.append(value)
                        value = ''

                if char == ':' and on_key == True: # Double check
                    on_key = False
                    on_value = True

                if char == ',' and on_value == True:
                    value_array.append(value)
                    value = ''

                if char not in ['%',':',' ','\n',',','&']:
                    if on_key:
                        key += char
                    elif on_value:
                        value += char
        if len(value_array) != 0: # Arrays (years, months) or single values
            out_dict[key] = value_array 
        else:
            if value != 'None':
                out_dict[key] = value
            else:
                out_dict[key] = ''
    return out_dict

## ---- Json I/O ----

def jsonWrite(path, file, content):
    """
    Simple Json Writing Function that handles all I/O
     - Writes a python dict to json file
    """
    if not os.path.exists(path):
        os.makedirs(path)

    g = open(path + '/' + file,'w')
    g.write(json.dumps(content))
    g.close()

def jsonRead(path, file):
    """
    Simple Json Reading Function that handles all I/O
     - Open file and read json data to python dict
    """
    g = open(path + '/' + file, 'r')
    content = json.load(g)
    g.close()
    return content


if __name__ == "__main__":
    basic(__file__)
