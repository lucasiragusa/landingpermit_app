from pathlib import Path
import time
import random
import pendulum
import sys
from datetime import datetime, timedelta

# Calculate the path to the 'src' directory
root_dir = Path(__file__).resolve().parent.parent
src_dir = root_dir / 'src'

# Add 'src' directory to sys.path
sys.path.append(str(src_dir))

from models.flight import Flight
from models.flight_series import FlightSeries

def parse_date(date_str):
    """
    Parses a date string in a specific format to a datetime object.

    Args:
        date_str (str): Date string in '01May23' format.

    Returns:
        datetime.date: Parsed date.
    """
    return pendulum.from_format(date_str, 'DDMMMYY')

def create_flights(flight_data, start_date, end_date, probability):
    """
    Creates a collection of Flight objects within a given date range based on a probability.

    Args:
        flight_data (dict): Data needed to construct a Flight object, excluding the departure date.
        start_date (str): Start date of the date range in '01May23' format.
        end_date (str): End date of the date range in '01May23' format.
        probability (float): Probability (between 0 and 1) of a flight occurring on each date.

    Returns:
        list: A list of Flight objects.
    """
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
    """
    Merges pairs of dictionary entries if they have the same value and represent consecutive weeks.

    Args:
        d (dict): A dictionary where keys are tuples representing week signatures and values are flight data.

    Returns:
        dict: A new dictionary with merged entries where applicable.
    """

    items = list(d.items())
    merged = False
    new_dict = {}

    i = 0
    while i < len(items) - 1:
        # Check if items are mergeable (same value and consecutive weeks)
        if items[i][1] == items[i + 1][1] and are_weeks_consecutive(items[i][0], items[i + 1][0]):
            new_key = (items[i][0][0], items[i + 1][0][1])
            new_dict[new_key] = items[i][1]
            i += 2  # Skip the next item as it's already merged
            merged = True
        else:
            new_dict[items[i][0]] = items[i][1]
            i += 1

    if i == len(items) - 1:
        new_dict[items[i][0]] = items[i][1]

    if merged:
        return merge_dict_pairs(new_dict)
    else:
        return new_dict


def iso_week_to_dates(year, week):
    """
    Convert ISO year and week number to the start and end dates of that week.

    Args:
        year (int): The year in which the week occurs.
        week (int): The ISO week number.

    Returns:
        tuple: A tuple containing the start and end dates of the week.
    """
    jan4 = datetime(year, 1, 4)
    start_of_week = jan4 - timedelta(days=jan4.isoweekday() - 1) + timedelta(weeks=week - 1)
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.date(), end_of_week.date()

def transform_week_signatures(d):
    """
    Transforms week signatures to a more readable format by converting them to start and end dates.

    Args:
        d (dict): A dictionary with keys as week signatures and values as some associated data.

    Returns:
        dict: A new dictionary with transformed keys.
    """

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
    """
    Writes flight data to a file.

    Args:
        flights (list): A list of Flight objects to be written.
        filename (str): The name of the file where data will be written.
        header (str): The header to be written at the top of the file.
        mode (str, optional): File opening mode. Defaults to 'a' (append mode).

    This function writes each flight object to the specified file in a human-readable format.
    """

    with open(filename, mode) as file:
        file.write(header + '\n')
        for flight in flights:
            file.write(str(flight) + '\n')
            
# Convert and write flights_by_week to the same file
def write_flights_by_week_to_file(flights_by_week, filename, header, mode='a'):
    """
    Writes flight data organized by week to a file.

    Args:
        flights_by_week (dict): A dictionary with week signatures as keys and lists of flights as values.
        filename (str): The name of the file where data will be written.
        header (str): The header to be written at the top of the section in the file.
        mode (str, optional): File opening mode. Defaults to 'a' (append mode).

    This function writes the flight data categorized by week to the specified file.
    """

    with open(filename, mode) as file:
        file.write('\n' + header + '\n')
        for week, flight_list in flights_by_week.items():
            file.write(f'{week}: {flight_list}\n')

def write_transformed_flights_to_file(transformed_flights, filename, header, mode='a'):
    """
    Writes transformed flight data to a file.

    Args:
        transformed_flights (dict): A dictionary with transformed flight data.
        filename (str): The name of the file where data will be written.
        header (str): The header to be written at the top of the section in the file.
        mode (str, optional): File opening mode. Defaults to 'a' (append mode).

    This function writes the transformed flight data, such as minimal representation, to the specified file.
    """

    with open(filename, mode) as file:
        file.write('\n' + header + '\n')
        for key, value in transformed_flights.items():
            file.write(f'{key}: {value}\n')

def format_dow_string (dow_string): 
    """
    Formats a string representing days of the week into a standardized dot notation.

    Args:
        dow_string (str): A string containing numbers representing days of the week.

    Returns:
        str: A formatted string where each number represents a day of the week and dots represent days without flights.

    Example:
        Input: '135'
        Output: '1.3.5..'
    """
    result = ''
    
    for i in range (1,8): 
        if str(i) in dow_string: 
            result += str(i)
        else: 
            result += '.'
    
    return result

def are_weeks_consecutive(week1, week2):
    """
    Check if two week signatures represent consecutive weeks.

    Args:
        week1 (tuple): The first week signature, e.g., ('2023_5', '2023_5').
        week2 (tuple): The second week signature, e.g., ('2023_10', '2023_10').

    Returns:
        bool: True if the weeks are consecutive, False otherwise.
    """
    import datetime

    def is_53_week_year(year):
        """
        Determine if a year has 53 weeks.
        """
        last_day_of_year = datetime.date(year, 12, 31)
        # A year has 53 weeks if the last day of the year or the day before is a Thursday
        return last_day_of_year.weekday() == 3 or (last_day_of_year - datetime.timedelta(days=1)).weekday() == 3

    year1, week_num1 = map(int, week1[1].split('_'))
    year2, week_num2 = map(int, week2[0].split('_'))

    if year1 == year2:
        return week_num1 + 1 == week_num2

    if year1 + 1 == year2:
        last_week_of_year = 53 if is_53_week_year(year1) else 52
        return week_num1 == last_week_of_year and week_num2 == 1

    return False


def get_first_day_of_isoweek(week_signature):
    # Split the week signature into year and week components
    year, week = map(int, week_signature.split('_'))

    # Creating a date object for January 1st of the given year
    date = pendulum.datetime(year, 1, 1)

    # Adjusting to the first day of the ISO week
    # ISO weeks start on Monday and belong to the year that has the majority of its days in the week
    while date.isocalendar()[1] != week or date.isocalendar()[0] != year:
        date = date.add(days=1)

    return date

def adjust_dow_outside_range(week_signature, dow_string, start_date, end_date): 
    """
    Adjusts a days-of-week string to exclude days outside a specified date range.

    Args:
        week_signature (str): A string representing the ISO week, used to determine the week's start day.
        dow_string (str): A string representing days of the week, where each character is a day (1-7) or '.'.
        start_date (date): The start date of the range.
        end_date (date): The end date of the range.

    Returns:
        str: The adjusted days-of-week string, modified to exclude days outside the specified date range.
    """
    dow_string = format_dow_string(dow_string)
    
    # Convert the dow_string to a list for modification
    dow_list = list(dow_string)
    week_start_day = get_first_day_of_isoweek(week_signature)
    result_list = [] # This will be the list that we return
    
    for i in range(0, 7):
        interim_day = week_start_day + timedelta(days=i)
        if interim_day < start_date or interim_day > end_date:
            result_list.extend(str(i+1))
        elif dow_list[i] != '.':
            result_list.extend(str(i+1))
        else: 
            result_list.extend('.')
    
    # Convert the list back to a string
    result_string = ''.join(result_list)
    return result_string

def adjust_dates_outside_range(my_dict, min_dep_date, max_dep_date):
    """
    Adjusts the keys of a dictionary to ensure the dates fall within a specified range.

    Args:
        my_dict (dict): The dictionary with tuple keys representing date ranges.
        min_dep_date (str): The minimum departure date, in a format parseable by parse_date.
        max_dep_date (str): The maximum departure date, in a format parseable by parse_date.

    Returns:
        dict: A new dictionary with adjusted keys to ensure dates fall within the specified range.
    """
    min_dep_date = parse_date(min_dep_date)
    max_dep_date = parse_date(max_dep_date)
    adjusted_dict = {}

    for key, value in my_dict.items():
    
        first_date_str, second_date_str = key
        first_date = parse_date(first_date_str)
        second_date = parse_date(second_date_str)

        # Adjusting the first and second date
        adjusted_first_date = max(first_date, min_dep_date).format('DDMMMYY')
        adjusted_second_date = min(second_date, max_dep_date).format('DDMMMYY')

        # Creating the new key and assigning the value from the old key
        new_key = (adjusted_first_date, adjusted_second_date)
        adjusted_dict[new_key] = value

    return adjusted_dict


# TESTING

if __name__ == '__main__':

    start_time = time.time() 
    
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
    end_date = '09May23'
    probability = 0.98  # chance of a flight occurring on any given day
    flights = create_flights(flight_base_data, start_date, end_date, probability)
    print (f'{len(flights)} flights created')

    if len(flights) == 0:
        print('No flights created. Exiting...')
        sys.exit()

    # Call the function after flights are created
    write_flights_to_file(flights, 'flights_all_stages.txt', '--- Stage 1: Flights Created ---', mode='w')

    # Take lowest and highest departure date from list of flights 
    min_dep_date = min(flights, key=lambda x: parse_date(x.departure_date)).departure_date
    max_dep_date = max(flights, key=lambda x: parse_date(x.departure_date)).departure_date

    # Define format string for desired format
    date_format = "%d%b%y"

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
            # Check if there's a flight on this weekday
            for flight in flight_list:
                if (flight.weekday == weekday):
                    flights_by_week_new[week] += str(weekday)

    # Format all dow strings to have a dot notation
    for week, dow_string in flights_by_week_new.items():
        flights_by_week_new[week] = format_dow_string(dow_string)
    
    flights_by_week = {(key, key): value for key, value in flights_by_week_new.items()}
    
    write_flights_by_week_to_file(flights_by_week, 'flights_all_stages.txt', '--- Stage 2: Flights by Week ---')
    
    # Now handle dates that are outside the range of start and end date
    adjusted_dictionary = {
        week_signature: adjust_dow_outside_range(week_signature[0], dow_string, start_date, end_date)
        for week_signature, dow_string in flights_by_week.items()
    }

    flights_by_week = adjusted_dictionary.copy()
     
    # Write intermediate step for debugging purposes
    write_flights_by_week_to_file(flights_by_week, 'flights_all_stages.txt', '--- Stage 2.5: Flights by Week after handling dates outside range ---')
    
    print ("Done writing intermediate step")
    
    # Now we need to merge consecutive weeks that have the same weekday pattern
    transformed_flights = transform_week_signatures(merge_dict_pairs(flights_by_week))

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    
    transformed_flights = adjust_dates_outside_range(transformed_flights, min_dep_date, max_dep_date)
    transformed_flights = dict(sorted(transformed_flights.items(), key=lambda x: parse_date(x[0][0])))

    # Assuming transformed_flights is a list or similar iterable
    write_transformed_flights_to_file(transformed_flights, 'flights_all_stages.txt', f'--- Stage 3: Flight Series Minimal Representation --- Elapsed time: {elapsed_time} seconds')
    

    #TODO: Add an additional piece of logic to ensure that we are showing the minimum representation: 
        # Count the contiguous number of days with consecutive flights. 
        # If the number of intervals resulting from using the with consecutive flights representation is less than the number of intervals represented
        # with the dot notation, then we should use the consecutive flights representation.
    
    #TODO: Turn this test case into a function that can be called on a list of flights that don't include a single type of flights 