from models.flight import Flight

class FlightHandler:
    def __init__(self):
        self.flights = []

    def add_flight(self, flight_data):
        """
        Adds a flight to the flight collection.

        Parameters:
        flight_data (dict): Data required to create a Flight object.
        """
        flight = Flight(flight_data)
        self.flights.append(flight)

    def filter_flights(self, **criteria):
        """
        Filters flights based on given criteria.

        Parameters:
        criteria (dict): Keyword arguments where keys are attribute names of Flight objects
                         and values are the corresponding values to filter by.

        Returns:
        List[Flight]: List of flights that match the criteria.
        """
        filtered_flights = self.flights
        for attribute, value in criteria.items():
            filtered_flights = [flight for flight in filtered_flights if getattr(flight, attribute, None) == value]

        return filtered_flights

    def group_flights(self, flight_list, attributes=None):
        
        if attributes is None:
            attributes = ['airline_designator', 'flight_number', 'service_type',
                          'departure_station_iata_code', 'departure_time', 'arrival_station_iata_code',
                          'arrival_time', 'equipment', 'aircraft_configuration']

        grouped_flights = {}

        for flight in flight_list:
            key = tuple(getattr(flight, attr) for attr in attributes)
            if key in grouped_flights:
                grouped_flights[key].append(flight)
            else:
                grouped_flights[key] = [flight]

        return grouped_flights

    def __str__(self):
        return f'FlightHandler with {len(self.flights)} flights'
