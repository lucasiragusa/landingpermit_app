import pendulum
import pandas as pd
from collections import namedtuple
import sys
from iata_season import IATA_Season

class SSIM_File: 
    '''This class initiates a SSIM file object. 
    It takes a single df to initiate, and then takes the result of the ssim_interpreter to 
    create attributes for the object (UTC, local, start/end date etc.)
    '''

    def __init__(self, ssim_file):
        self.ssim_file = ssim_file
        self.timezone_mode = None
        self.start_date = None
        self.end_date = None
        self.exported_date = None
        self.iata_seasons = None
        self.df = None
        
        self._get_ssim_attributes()
        self._get_col_data()
        self.get_iata_seasons()

        self._get_ssim_df(ssim_file, *self._get_col_data())
               

    def _get_ssim_attributes(self): 
        '''
        This function takes an SSIM file and returns a dictionary with the main attributes of the file.
        For example, it tells if the file is in local or UTC mode, the start and end date of the file in local and utc, etc
        The idea of this function is that it will be used to create a SSIMFile object 
        '''
        
        with open(self.ssim_file, 'r') as file:
            for line in file:
                if line.startswith('2'):
                    self.timezone_mode = 'local' if line[1] == 'L' else 'UTC' if line[1] == 'U' else None
                    
                    start_date_str = line[14:21].title()  # Convert to format with first letter capital
                    self.start_date = pendulum.from_format(start_date_str, "DDMMMYY")

                    end_date_str = line[21:28].title()  # Convert to format with first letter capital
                    self.end_date = pendulum.from_format(end_date_str, "DDMMMYY")

                    try:
                        exported_date_str = line[28:35].title()  # Convert to format with first letter capital
                        self.exported_date = pendulum.from_format(exported_date_str, "DDMMMYY")
                    except:
                        self.exported_date = None
                    
                    # Once we find and process the line starting with '2', we can break out of the loop
                    break



    # Named tuple for column length
    @staticmethod
    def _get_col_data():

        '''
        Defines the cosnstants necessary to extract data from the fixed width file
        '''

        Position = namedtuple('Position', ['start', 'end'])


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

        return col_length, col_headers, cols_to_keep
    
    
    def _get_ssim_df(self, filename, col_length, col_headers, cols_to_keep):
        df = pd.read_fwf(filename, colspecs=col_length, header=None, names=col_headers)
        # Filter rows for flights
        df = df[df['Record type'] == 3]
        df = df[cols_to_keep]
        df['Arvl time (pax)'] = df['Arvl time (pax)'].apply(lambda x: str(int(x)).zfill(4))
        df['Flight number'] = df.apply(lambda x: x['Airline designator'] + '  ' + str(x['Flight number']).zfill(4), axis=1)
        df.drop(columns=['Airline designator'], inplace=True)
        df.reset_index(drop=True, inplace=True)

        self.df = df

    def get_iata_seasons(self):
        seasons = []

        # Helper function to determine the season of a given date
        def determine_season(date):
            summer_start = pendulum.datetime(date.year, 3, 31, 0, 0, 0).last_of('month', day_of_week=pendulum.SUNDAY)
            winter_start = pendulum.datetime(date.year, 10, 31, 0, 0, 0).last_of('month', day_of_week=pendulum.SUNDAY)
            
            if summer_start <= date < winter_start:
                return 'S' + str(date.year)[2:]
            else:
                if date < summer_start:
                    return 'W' + str(date.year - 1)[2:]
                else:
                    return 'W' + str(date.year)[2:]

        # Identify the season of the start and end dates
        start_season = determine_season(self.start_date)
        end_season = determine_season(self.end_date)

        # Now fill in the seasons in between
        current_season = start_season
        while current_season != end_season:
            seasons.append(current_season)

            # Move to the next season
            if 'S' in current_season:
                current_season = 'W' + current_season[1:]
            else:
                year = int(current_season[1:]) + 1
                current_season = 'S' + str(year).zfill(2)
        
        # Add the end season and return
        seasons.append(end_season)

        self.iata_seasons = [IATA_Season(season) for season in seasons]


# Test code
if __name__ == '__main__':
    import sys
    import time
    import pendulum

    ssim = sys.argv[1]

    start_time = time.time()  # Start the timer

    ssim_object = SSIM_File(ssim)

    # for attribute, value in ssim_object.__dict__.items():
    #     print(f"{attribute}: {value}")

    print(ssim_object.iata_seasons)

    elapsed_time = time.time() - start_time  # Calculate elapsed time

    print(f"\nTime taken to execute read_ssim: {elapsed_time:.2f} seconds")