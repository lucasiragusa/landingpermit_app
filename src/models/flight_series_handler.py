
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.flight_series import FlightSeries
from models.airport import Airport
from models.airport import airport_data
from models.flight import Flight
from models.ssim_file import SSIM_File
from utils.pendulum_helper import pendulum_to_string, reformat_date_signature, parse_date
import pendulum


class FlightSeriesHandler:
    def __init__(self):
        self.flight_series_collection = []


    def create_flight_series_from_df(self, df):
        for _, row in df.iterrows():
            flight_series_data = row.to_dict()
            flight_series = FlightSeries(flight_series_data)
            self.flight_series_collection.append(flight_series)
        return self.flight_series_collection


    def get_unique_countries(self):
        """Return a set of all unique countries from the flight series."""

        # Using a helper function to determine the country of an airport.
        def get_country(airport_code):
            # Extracting country code from the airport_data dictionary.
            return airport_data[airport_code]['ISO country']  # Adjust this if the value in the dictionary is an object
            
        countries = set()

        for series in self.flight_series_collection:
            departure_country = get_country(series.departure_station.iata_code)
            arrival_country = get_country(series.arrival_station.iata_code)

            # Add to the set. If the country is already in the set, it won't create a duplicate.
            countries.add(departure_country)
            countries.add(arrival_country)

        # Filter out any None values which might come from airports not present in airport_data
        countries.discard(None)
        
        return countries

    def add_flight_series(self, flight_series_data):
        flight_series = FlightSeries(flight_series_data)
        self.flight_series_collection.append(flight_series)

    def search_by_attribute(self, attribute, value):
        # Return flight series with a specific attribute value
        return [fs for fs in self.flight_series_collection if getattr(fs, attribute) == value]

    def count_flights(self):
        # Check for overlapping flight series
        pass

    def calculate_duration(self, flight_series):
        # Calculate and return the duration of a specific flight series in days
        pass

    def filter_by_country(self, country_code):
        """Filter flight series by either departure or arrival country."""

        # Using a helper function to determine the country of an airport.
        def get_country(airport):
            # Extracting country code from the airport_data dictionary.
            iata_code = airport.iata_code
            return airport_data.get(iata_code)['ISO country']
                
        filtered_series = [
            series 
            for series in self.flight_series_collection 
            if get_country(series.departure_station) == country_code or get_country(series.arrival_station) == country_code
        ]

        return filtered_series

    def parse_date(date_str):
        """
        Parses a date string in a specific format to a datetime object.

        Args:
            date_str (str): Date string in '01May23' format.

        Returns:
            datetime.date: Parsed date.
        """
        return pendulum.from_format(date_str, 'DDMMMYY')

    def de_serialize_flight_series(self, flight_series_collection):
        '''
        Converts a collection of FlightSeries objects to a list of flight objects.   
        '''
        
        flight_collection = [] #Declare the output flight collection
        
        if len(self.flight_series_collection) == 0:
            raise ValueError('No flight series in collection.')
        
        for series in self.flight_series_collection:
            print (f'effective date: {series.effective_date}')  #debug
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
    