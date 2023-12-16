import random
import datetime
from models.flight import Flight  # Assuming you have a Flight class defined in models/flight.py

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
    'Service Type': 'Scheduled Pax',
    'Dept Stn': {'iata_code': 'JFK', 'name': 'John F Kennedy International Airport'},
    'Dept time (pax)': '08:00',
    'Arvl Stn': {'iata_code': 'LAX', 'name': 'Los Angeles International Airport'},
    'Arvl time (pax)': '11:00',
    'Equipment': 'Boeing 737',
    'Aircraft configuration': 'Economy/Business'
}

start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 1, 10)
probability = 0.5  # 50% chance of a flight occurring on any given day

flights = create_flights(flight_base_data, start_date, end_date, probability)
for flight in flights:
    print(flight)
