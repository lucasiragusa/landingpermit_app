import pandas as pd
from collections import namedtuple
import sys

# Named tuple for column length
Position = namedtuple('Position', ['start', 'end'])

def get_col_data():
    col_headers = ['Record type','Operational suffix',
    'Airline designator','Flight number',
    'Itinerary variation identifier','Leg sequence Number',
    'Service Type','Eff','Dis',
    'Day(s) of operation','Frequency rate','Dept Stn',
    'Dept time (pax)','Dept time (AC)',
    'UTC/Local Time variation (dept)','Passenger dept terminal',
    'Arvl Stn','Arvl time (AC)','Arvl time (pax)',
    'UTC/Local Time variation','Passenger arvl terminal',
    'Equipment','PRBD','PRBM','Meal service note',
    'Joint operation Airline designators',
    'MCT Status','Secure flight Indicator',
    'Itinerary variation identifier Overflow','Aircraft owner',
    'Cockpit crew employer','Cabin crew employer',
    'Onward Airline designator','Onward Flight number',
    'Aircraft rotation layover','Onward Operational suffix',
    'Automated Check-in','Flight transit layover',
    'Operating airline','Traffic restriction code',
    'Traffic restriction code leg overflow indicator',
    'Aircraft configuration','Date variation',
    'Record serial number']
    cols_to_keep = [
    'Airline designator',
    'Flight number',
    'Service Type',
    'Eff',
    'Dis',
    'Day(s) of operation',
    'Dept Stn',
    'Dept time (pax)', 
    'Arvl Stn',
    'Arvl time (pax)',
    'Equipment', 
    'Aircraft configuration']

    col_length_data = [(0,1),(1,2),
    (2,5),(5,9),
    (9,11),(11,13),
    (13,14),(14,21),(21,28),
    (28,35),(35,36),(36,39),
    (39,43),(43,47),
    (47,52),(52,54),
    (54,57),(57,61),(61,65),
    (65,70),(70,72),
    (72,75),(75,95),(95,100),(100,110),
    (110,119),
    (119,121),(121,122),
    (127,128),(128,131),
    (131,134),(134,137),
    (137,140),(140,144),
    (144,145),(145,146),
    (146,147),(147,148),
    (148,149),(149,160),
    (160,161),
    (172,192),(192,194),
    (194,200)]

    col_length = [Position(*data) for data in col_length_data]

    return col_headers, cols_to_keep, col_length

def read_and_filter_ssim(filename, col_length, col_headers, cols_to_keep):
    print ('About to read file')
    df = pd.read_fwf(filename, colspecs=col_length, header=None, names=col_headers)
    print ('File read')
    # Filter rows for flights
    df = df[df['Record type'] == 3]
    df = df[cols_to_keep]
    df['Arvl time (pax)'] = df['Arvl time (pax)'].apply(lambda x: str(int(x)).zfill(4))
    df['Flight number'] = df.apply(lambda x: x['Airline designator'] + '  ' + str(x['Flight number']).zfill(4), axis=1)
    df.drop(columns=['Airline designator'], inplace=True)

    return df

def read_ssim(ssim):
    col_headers, cols_to_keep, col_length = get_col_data()
    df = read_and_filter_ssim(ssim, col_length, col_headers, cols_to_keep)
    
    print (df.head())
    return df

# Test code
if __name__ == '__main__':
    import sys
    import time

    print ('Started...')
    # print(f"Argument: {sys.argv[0]}")
    ssim = sys.argv[1]

    start_time = time.time()  # Start the timer

    read_ssim(ssim)

    elapsed_time = time.time() - start_time  # Calculate elapsed time

    print(f"Time taken to execute read_ssim: {elapsed_time:.2f} seconds")

