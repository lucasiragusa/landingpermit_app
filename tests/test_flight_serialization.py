import random
import datetime
from models.flight import Flight

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

# Example usage
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

if __name__ == '__main__':

    start_date = datetime.date(2022, 12, 1)
    end_date = datetime.date(2023, 5, 10)
    probability = 0.95  # 50% chance of a flight occurring on any given day

    flights = create_flights(flight_base_data, start_date, end_date, probability)
    for flight in flights:
        print(flight)
