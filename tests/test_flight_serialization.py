import sys
from pathlib import Path

# Calculate the path to the 'src' directory
root_dir = Path(__file__).resolve().parent.parent
src_dir = root_dir / 'src'

# Add 'src' directory to sys.path
sys.path.append(str(src_dir))

import random
import pendulum
import pandas as pd
from models.flight import Flight
from datetime import datetime, timedelta



def create_flights(flight_data, start_date, end_date, probability):
    """
    Creates a collection of Flight objects within a given date range based on a probability.

    Args:
        flight_data (dict): Data needed to construct a Flight object, excluding the departure date.
        start_date (datetime.date): Start date of the date range.
        end_date (datetime.date): End date of the date range.
        probability (float): Probability (between 0 and 1) of a flight occurring on each date.

    Returns:
        list: A list of Flight objects.
    """
    flights = []  
    current_date = start_date
    while current_date <= end_date:
        if random.random() < probability:
            flight_data_for_day = flight_data.copy()
            flight_data_for_day['Departure Date'] = current_date.strftime('%Y-%m-%d')
            flights.append(Flight(flight_data_for_day))
        current_date += datetime.timedelta(days=1)
    return flights


def parse_date(date_str):
    # Parse a date string in '01May23' format
    return pendulum.from_format(date_str, 'DDMMMYY')

def create_flights(flight_data, start_date, end_date, probability):
    flights = []
    current_date = pendulum.from_format(start_date, 'DDMMMYY')
    end_date = pendulum.from_format(end_date, 'DDMMMYY')
        
    while current_date <= end_date:
        if random.random() < probability:
            # Update the departure date in the flight data
            updated_flight_data = flight_data.copy()
            updated_flight_data['Departure Date'] = current_date.strftime('%d%b%y')

            # Create a Flight object
            flight = Flight(updated_flight_data)
            flights.append(flight)

        current_date = current_date.add(days=1)
    
    return flights


def merge_dict_pairs(d):
    items = list(d.items())
    merged = False
    new_dict = {}

    i = 0
    while i < len(items):
        if i + 1 < len(items) and items[i][1] == items[i + 1][1]:
            # Create a new key with the first element of the first key and the last element of the second key
            new_key = (items[i][0][0], items[i + 1][0][-1])
            new_dict[new_key] = items[i][1]
            i += 2  # Skip the next item as it's already merged
            merged = True
        else:
            new_dict[items[i][0]] = items[i][1]
            i += 1

    # If a merge occurred, we need to check for further possible merges
    if merged:
        return merge_dict_pairs(new_dict)
    else:
        return new_dict


def iso_week_to_dates(year, week):
    """Convert ISO year and week number to the start and end dates of that week."""
    jan4 = datetime(year, 1, 4)
    start_of_week = jan4 - timedelta(days=jan4.isoweekday() - 1) + timedelta(weeks=week - 1)
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.date(), end_of_week.date()

def transform_week_signatures(d):
    new_dict = {}
    for key, value in d.items():
        start_year, start_week = map(int, key[0].split('_'))
        end_year, end_week = map(int, key[1].split('_'))

        # Adjust for year transition only if the end week is from the next year
        if end_week == 1 and start_week > 50:
            end_year = start_year + 1

        start_date, _ = iso_week_to_dates(start_year, start_week)
        _, end_date = iso_week_to_dates(end_year, end_week)

        start_date_str = start_date.strftime("%d%b%y")
        end_date_str = end_date.strftime("%d%b%y")

        new_dict[(start_date_str, end_date_str)] = value

    return new_dict

def write_flights_to_file(flights, filename, header, mode='a'):
    with open(filename, mode) as file:
        file.write(header + '\n')
        for flight in flights:
            file.write(str(flight) + '\n')
            
# Convert and write flights_by_week to the same file
def write_flights_by_week_to_file(flights_by_week, filename, header, mode='a'):
    with open(filename, mode) as file:
        file.write('\n' + header + '\n')
        for week, flight_list in flights_by_week.items():
            file.write(f'Week {week}: {flight_list}\n')

def write_transformed_flights_to_file(transformed_flights, filename, header, mode='a'):
    with open(filename, mode) as file:
        file.write('\n' + header + '\n')
        for key, value in transformed_flights.items():
            file.write(f'{key}: {value}\n')



if __name__ == '__main__':

    # Declare flights to be tested
    flight_base_data = {
    'Airline designator': 'XY',
    'Flight number': '123',
    'Service Type': 'J',
    'Dept Stn': 'JFK',
    'Dept time (pax)': '08:00',
    'Arvl Stn': 'LAX',
    'Arvl time (pax)': '11:00',
    'Equipment': '321',
    'Aircraft configuration': 'Y180'
    }
    
    # Build parameters for create_flights function
    start_date = '01Nov22'
    end_date = '02May23'
    probability = .8  # chance of a flight occurring on any given day
    flights = create_flights(flight_base_data, start_date, end_date, probability)
    print (f'{len(flights)} flights created')

    # Call the function after flights are created
    write_flights_to_file(flights, 'flights_all_stages.txt', '--- Stage 1: Flights Created ---', mode='w')  # 'w' to write from the beginning

    # Take lowest and highest departure date from list of flights 
    min_dep_date = min(flights, key=lambda x: x.departure_date).departure_date
    max_dep_date = max(flights, key=lambda x: x.departure_date).departure_date

    # Define format string for desired format
    date_format = "%d%b%y"

    # Print formatted dates
    print(f'{min_dep_date.format(date_format)} is the earliest departure date')
    print(f'{max_dep_date.format(date_format)} is the latest departure date')

    # Convert dates to pendulum objects for future use
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    
    # Create dictionary with keys equal to set of week signatures and values equal to list of flights in that week
    # TODO: after establishing if this works, clean up this section of the code
    flights_by_week = {}

    for flight in flights:
        if flight.week_signature not in flights_by_week:
            flights_by_week[flight.week_signature] = []
        flights_by_week[flight.week_signature].append(flight)
        
    flights_by_week_new = {}

    for week, flight_list in flights_by_week.items():
        flights_by_week_new[week] = ''
        
        for weekday in range(1, 8):
            # Check if there's a flight on this weekday or if the flight's departure date is outside the specified range
            if any(flight.weekday == weekday or parse_date(flight.departure_date) < parse_date(min_dep_date) or parse_date(flight.departure_date) > parse_date(max_dep_date) for flight in flight_list):
                flights_by_week_new[week] += str(weekday)
            else:
                flights_by_week_new[week] += '.'
    
    flights_by_week = {(key, key): value for key, value in flights_by_week_new.items()}
    
    write_flights_by_week_to_file(flights_by_week, 'flights_all_stages.txt', '--- Stage 2: Flights by Week ---')
    
    transformed_flights = transform_week_signatures(merge_dict_pairs(flights_by_week))

    # Assuming transformed_flights is a list or similar iterable
    write_transformed_flights_to_file(transformed_flights, 'flights_all_stages.txt', '--- Stage 3: Transformed Flights ---')
    

