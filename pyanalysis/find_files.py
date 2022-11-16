
##            DW Standard Python Library

##            Find multiple files in a dir

# Daniel Westwood (daniel.westwood@stfc.ac.uk)

# Updates:
#   - Added to standard python library (01/02/2021)
#   - Added list_files method   (04/02/2021)
#   - Concatenated file_import methods to find_files (08/07/2021)

# ------------------ find_files.py --------------------

import re
import os
import sys
import glob

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

def accept_input(prompt, accepted='', atype='', fileroot=''):
    if type(accepted) != list:
        accepted = [accepted]
    valid_entry = False
    while not valid_entry:
        user_in = input(prompt)
        if accepted == [''] or user_in in accepted:
            if atype == 'int':
                try:
                    user_in = int(user_in)
                    valid_entry = True
                except:
                    print('Error: Input does not meet "int" type requirements, please enter a number')
            elif atype == 'file':
                if os.path.isfile(fileroot+user_in):
                    valid_entry = True
                else:
                    print('Error: Requested file not found')
            else:
                valid_entry = True
        else: 
            print('Error: Input not in accepted form')
    return user_in

if __name__ == "__main__":
    print('pyanalysis: find_files.py')
