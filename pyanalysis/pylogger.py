# encoding: utf-8

__author__ = 'Daniel Westwood'
__date__ = '16 Nov 2022'
__copyright__ = 'Copyright 2022 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'daniel.westwood@stfc.ac.uk'

import os

def message(text):
    if os.getenv('PY_ANALYSIS_LOG') != "False":
        if type(text) == list:
            for line in text:
                print('PyAnalysis-log:',line.replace('\n',''))
        else:
            print('PyAnalysis-log:',text.replace('\n',''))

def basic(filepath):
    filename = filepath.split('/')[-1]
    module = filename.replace('.py','')
    
    message([filename,
        'No syntax issues',
        'To use routines, include "from {} import *" in your .py scripts'.format(module)
        ])

if __name__ == "__main__":
    basic(__file__)
