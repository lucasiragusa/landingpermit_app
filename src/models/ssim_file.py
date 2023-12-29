import pendulum
import pandas as pd
from collections import namedtuple
import sys
from models.ssim_file_reader import SSIMFileReader
from models.seasons_handler import DateSeasonHandler
from models.flight import Flight
from utils.pendulum_helper import parse_date, pendulum_to_string, reformat_date_signature


class SSIM_File: 
    '''This class initiates a SSIM file object. 
    It takes a single df to initiate, and then takes the result of the ssim_interpreter to 
    create attributes for the object (UTC, local, start/end date etc.)
    '''

    def __init__(self, ssim_file_path):
        
        from models.flight_series_handler import FlightSeriesHandler
        
        self.reader = SSIMFileReader(ssim_file_path)
        self.attributes = self.reader.get_attributes()
        attributes = self.reader.get_attributes()
        self.timezone_mode = attributes['timezone_mode']
        self.start_date = attributes['start_date']
        self.end_date = attributes['end_date']
        self.exported_date = attributes['exported_date']
        self.df = self.reader.get_dataframe(ssim_file_path, *self._get_col_data())
        self.season_handler = DateSeasonHandler(self.start_date, self.end_date)
        self.iata_seasons = self.season_handler.get_iata_seasons()
        self.flight_series_handler = FlightSeriesHandler()
        self.flight_series_list = self.flight_series_handler.create_flight_series_from_df(self.df)


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
    
    def export_to_csv(self, filename):
        self.df.to_csv(filename, index=False)

    # def de_serialize(self):
    #     '''
    #     Converts a collection of FlightSeries objects to a list of flight objects.   
    #     '''
    #     flight_collection = self.flight_series_list
        
    #     handler = self.flight_series_handler
        
    #     flight_list = handler.de_serialize_flight_series(flight_collection)
        
    #     return flight_list
    
    def de_serialize(self):
        
        '''
        Converts a collection of FlightSeries objects to a list of flight objects.   
        '''
        
        flight_series_collection = self.flight_series_list
        
        flight_collection = [] #Declare the output flight collection
        
        if len(flight_series_collection) == 0:
            raise ValueError('No flight series in collection.')
        
        for series in flight_series_collection:
            eff_date = reformat_date_signature(series.effective_date)
            dis_date = reformat_date_signature(series.discontinued_date)

            # Iterate over all dates in the flight series
            for date in pendulum.interval(parse_date(eff_date), parse_date(dis_date)).range('days'):
                # Check if the flight operates on the current date
                if str(date.isoweekday()) in series.days_of_operation:
                    # Create a flight object
                    flight_data = {
                        'Airline designator': series.airline_designator,
                        'Flight number': series.flight_number,
                        'Service Type': series.service_type,
                        'Departure Date': pendulum_to_string(date),
                        'Dept Stn': series.departure_station.iata_code,
                        'Dept time (pax)': series.departure_time,
                        'Arvl Stn': series.arrival_station.iata_code,
                        'Arvl time (pax)': series.arrival_time,
                        'Equipment': series.equipment,
                        'Aircraft configuration': series.aircraft_configuration
                    }
                    flight = Flight(flight_data)
                    flight_collection.append(flight)
        return flight_collection
