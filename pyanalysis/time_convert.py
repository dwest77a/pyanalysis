
##      DW Standard Python Library

##          Time Conversions

# Daniel Westwood (daniel.westwood@stfc.ac.uk)

# Updates:
#   - Updated comments (17/12/2020)
#   - separation of files (17/12/2020)

# -------------------- time_convert.py --------------------

# - Convert separate time increments to International Atomic Time (IAT)
# - Convert julian date to MJD then to IAT

## --- Module Imports --- ##

# - Time Conversion - #
import julian

## --- End Module Imports --- ##

def sep_to_IAT(year, month, day, hourset, minuteset):
	# Convert separate time increments to International Atomic Time (IAT)
	# year, month, day, hours, minutes -> IAT
	
    IATs = []
    for index, hour in enumerate(hourset):
        frac_day = ( float(hour)*3600 + float(minuteset[index]) *60)/86400 + float(day)
    
        if frac_day < 10:
            frac_day = '0' + str(frac_day)
        IATs.append( str(str(year)[2] + str(year)[3]) + str('%02d' % float(month)) + str(frac_day) )
    return IATs

def jd_to_IAT(julian_dates):
	# Convert a Julian Date to IAT (International Atomic Time)
	# Take example date as first in 2d array of dates,
	# convert this single date, and apply the simple conversion to all dates
	
	# Example jd
    jd = julian_dates[0][0]
    
    # Modified Julian Date mjd
    mjd = jd - 2400000.5
    
    # datetime object dt
    dt = julian.from_jd(mjd,fmt ='mjd')
    
    # number of days as fraction
    frac_day = (dt.hour*3600 + dt.minute*60 + dt.second)/86400 + dt.day
    
    # % convert to 2 dp
    if frac_day < 10:
        frac_day = '0' + str(frac_day)
    # IAT date
    IAT = str(str(dt.year)[2] + str(dt.year)[3]) + str('%02d' % dt.month) + str(frac_day)
    
    # set jd as point zero and calculate IATs based on initial plus change in date
    # faster use of numpy arrays to add to all values
    julian_dates = julian_dates - jd + float(IAT)
    return julian_dates
    
