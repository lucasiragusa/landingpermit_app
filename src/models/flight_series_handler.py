
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.flight_series import FlightSeries
from models.airport import Airport
from models.airport import airport_data
from models.ssim_file import SSIM_File
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