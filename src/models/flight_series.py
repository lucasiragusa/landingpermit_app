from models.airport import airport_data
from models.airport import Airport

class FlightSeries: 

    """
    Represents a series of flights, all of which share the same details. 
    It is a customary representation of scheduled flights in the airline industry. 
    Many instances of "Flight" objectes can be grouped as a flight series object so far 
    as they share the same attributes other than departure date. 

    Attributes:
        airline_designator (str): The IATA Designator of the Operating Airline.
        flight_number (str): The flight number. 
        service_type (str): SSIM-compliant Service type indicating the type of flight (e.g. scheduled pax, cargo, etc.)
        effective_date (str): The starting date from which the flight series is effective, in DDMMMYY format.
        discontinued_date (str): The date after which the flight series is no longer operational, in DDMMMYY format.
        days_of_operation (str): Days of the week on which the flight operates.(Monday = 1)
        departure_station (Airport): The airport from which the flight departs.
        departure_time (str): The scheduled departure time of the flight.
        arrival_station (Airport): The airport at which the flight arrives.
        arrival_time (str): The scheduled arrival time of the flight.
        equipment (str): Details about the flight's equipment.
        aircraft_configuration (str): Configuration of the aircraft used in the flight.

    Methods:
        __init__(flight_series_data): Constructs the FlightSeries object with provided flight series data.
        __repr__(): Returns a string representation of the FlightSeries object.
        to_dict(): Converts the FlightSeries object to a dictionary representation.

    The FlightSeries is initialized with a dictionary containing the flight series data.
    Each attribute of the class represents a key aspect of the flight series information.
    """

    def __init__(self, flight_series_data):
        
        self.airline_designator = flight_series_data['Airline designator']
        self.flight_number = flight_series_data['Flight number']
        self.service_type = flight_series_data['Service Type']
        self.effective_date = flight_series_data['Eff']
        self.discontinued_date = flight_series_data['Dis']
        self.days_of_operation = flight_series_data['Day(s) of operation']
        self.departure_station = Airport(flight_series_data['Dept Stn'])
        self.departure_time = flight_series_data['Dept time (pax)']
        self.arrival_station = Airport(flight_series_data['Arvl Stn'])
        self.arrival_time = flight_series_data['Arvl time (pax)']
        self.equipment = flight_series_data['Equipment']
        self.aircraft_configuration = flight_series_data['Aircraft configuration']
        #Add count of Flights in flight series
        #Add time mode (local/UTC) in arguments to constructor
        #Add IATA Season

    def __repr__(self):
        
        self.days_of_operation = self.days_of_operation.replace(' ', '')
        temp_string = ''
        for i in range (1,8): 
            if str(i) in self.days_of_operation:
                temp_string += str(i)
            else: 
                temp_string += '.'
        self.days_of_operation = temp_string
        
        return f"{self.airline_designator} {self.flight_number}: {self.departure_station}-{self.arrival_station} ({self.effective_date}-{self.discontinued_date}) {self.days_of_operation}"
    
    def to_dict(self):
        return {
            'Airline designator': self.airline_designator,
            'Flight number': self.flight_number,
            'Service Type': self.service_type,
            'Eff': self.effective_date,
            'Dis': self.discontinued_date,
            'Day(s) of operation': self.days_of_operation,
            'Dept Stn': self.departure_station.iata_code,
            'Dept time (pax)': self.departure_time,
            'Arvl Stn': self.arrival_station.iata_code,
            'Arvl time (pax)': self.arrival_time,
            'Equipment': self.equipment,
            'Aircraft configuration': self.aircraft_configuration
        }