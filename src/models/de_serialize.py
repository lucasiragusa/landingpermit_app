import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.flight_series_handler import FlightSeriesHandler
from models.airport import airport_data
from models.ssim_file import SSIM_File
from models.flight import Flight
from utils.pendulum_helper import get_date_range, pendulum_to_string, parse_date, reformat_date_signature, get_weekday


def de_serialize(ssim_path):
        
        # Declare empty Flight objects set 
        flights = set()
        
        # De-serialize a flight series into a set of flights
        ssim_object = SSIM_File(ssim_path)
        handler = FlightSeriesHandler()

        # Take effective and discountinue date, and create a list of dates in between
        flight_series = handler.create_flight_series_from_df(ssim_object.df)

        # For each flight series object, create however many flight object are necessary
        for series in flight_series:
            # print (f'Checking for flight series: {series}')
            
            # Get the dates in between the effective and discountinue date
            n_days = get_date_range(reformat_date_signature(series.effective_date), reformat_date_signature(series.discontinued_date))
            effective_date = parse_date(reformat_date_signature(series.effective_date))
            
            # For each date, create a flight object and append to set if the corresponding day of operation is a number and not a .
            
            for day in range(n_days):
                # If the day of operation is a number, create a flight object
                date = effective_date.add(days=day) # -1 because the first day is the effective date
                
                # print(f'Checking for date {date}')
                # print(f'Weekday is {get_weekday(date)}')
                # print(f'Days of operation are {series.days_of_operation}')
                
                if str(get_weekday(date)) in series.days_of_operation:
                    # print ('Positive Match, creating flight object...')
                    
                    # Create a flight object
                    flight_dict = {}
                    flight_dict ['Airline designator'] = series.airline_designator
                    flight_dict ['Flight number'] = series.flight_number
                    flight_dict ['Service Type'] = series.service_type
                    flight_dict ['Departure Date'] = pendulum_to_string(date)
                    flight_dict ['Dept Stn'] = series.departure_station.iata_code
                    flight_dict ['Dept time (pax)'] = series.departure_time
                    flight_dict ['Arvl Stn'] = series.arrival_station.iata_code
                    flight_dict ['Arvl time (pax)'] = series.arrival_time
                    flight_dict ['Equipment'] = series.equipment
                    flight_dict ['Aircraft configuration'] = series.aircraft_configuration
                    
                    flight = Flight(flight_dict)
                    
                    # Add the flight object to the set
                    flights.add(flight)
        
        return flights
                    
# if __name__ == '__main__':
    
#     # Create a flight series handler
#     from pathlib import Path

#     base_dir = Path(__file__).resolve().parent.parent.parent
#     ssim_path = base_dir / 'data' / 'ssim' / 'EY_SSIM_base_compare.ssim'
    
#     de_serialize(ssim_path)
        
