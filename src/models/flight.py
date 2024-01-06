# TODO: What shall this be about?
# A flight series is a series of flights that have the same exact characteristics 
# (same origin, destination, flight number, departure time, arrival time, season etc.)
# But fundamentally it is made up by individual flights, this class is supposed to represent individual flights 
# It will be useful in the part where we compare the base ssim with the alt ssim and output only the flights that changed

import pendulum

from src.models.airport import Airport, airport_data

class Flight:
    """
    Represents a single flight. This class has similar attributes to the FlightSeries class,
    but instead of a series of flights, it represents a single flight with a specific departure date.

    Attributes:
        airline_designator (str): The IATA Designator of the Operating Airline.
        flight_number (str): The flight number.
        service_type (str): SSIM-compliant Service type indicating the type of flight (e.g. scheduled pax, cargo, etc.)
        departure_date (str): The departure date of the flight. (DDMMMYY)
        departure_station (Airport): The airport from which the flight departs.
        departure_time (str): The scheduled departure time of the flight.
        arrival_station (Airport): The airport at which the flight arrives.
        arrival_time (str): The scheduled arrival time of the flight.
        equipment (str): Details about the flight's equipment.
        aircraft_configuration (str): Configuration of the aircraft used in the flight.
        isocalendar (tuple): A tuple containing the year, week number and weekday of the flight's departure date.
        year (int): The year of the flight's departure date.
        isoweek (int): The week number of the flight's departure date.
        weekday (int): The weekday of the flight's departure date.
        week_signature (str): A string containing the year and week number of the flight's departure date.
        unique_id (str): A unique identifier for the flight.
        change_status (str): Indicates if the flight has been added, deleted or modified.
    """

    def __init__(self, flight_data):
        
        # Arguments that must be in flight_data:
        self.airline_designator = flight_data['Airline designator']
        self.flight_number = flight_data['Flight number']
        self.service_type = flight_data['Service Type']
        self.departure_date = flight_data['Departure Date']
        self.departure_station = Airport(flight_data['Dept Stn'])
        self.departure_station_iata_code = flight_data['Dept Stn']
        self.departure_time = flight_data['Dept time (pax)']
        self.arrival_station = Airport(flight_data['Arvl Stn'])
        self.arrival_station_iata_code = flight_data['Arvl Stn']
        self.arrival_time = flight_data['Arvl time (pax)']
        self.equipment = flight_data['Equipment']
        self.aircraft_configuration = flight_data['Aircraft configuration']
        self.departure_country = airport_data.get(self.departure_station_iata_code)['ISO country']
        self.arrival_country = airport_data.get(self.arrival_station_iata_code)['ISO country']
        
        # Arguments that can be calculated from the above:
        self.isocalendar = pendulum.from_format(self.departure_date, 'DDMMMYY').isocalendar()
        self.year = self.isocalendar[0]
        self.isoweek = self.isocalendar[1]
        self.weekday = self.isocalendar[2]
        self.week_signature = str(self.year) + '_' + str(self.isoweek).zfill(2)
        self.unique_id = self.flight_number + '_' + self.departure_date
        self.change_status = None

    def __repr__(self):
        return f'{self.flight_number} {self.departure_date} {self.departure_time} {self.arrival_time} ({self.week_signature}) Weekday: {self.weekday}'

    def __str__(self) -> str:
        return f'{self.flight_number} {self.departure_date} {self.departure_station}-{self.arrival_station} {self.departure_time} {self.arrival_time} ({self.week_signature}) Weekday: {self.weekday}'
    
    def __eq__(self, other):
        if not isinstance(other, Flight):
            return False

        return (self.airline_designator == other.airline_designator and
                self.flight_number == other.flight_number and
                self.service_type == other.service_type and
                self.departure_date == other.departure_date and
                self.departure_station == other.departure_station and
                self.departure_time == other.departure_time and
                self.arrival_station == other.arrival_station and
                self.arrival_time == other.arrival_time and
                self.equipment == other.equipment and
                self.aircraft_configuration == other.aircraft_configuration)

    def __hash__(self):
        return hash((self.airline_designator, self.flight_number, self.service_type,
                     self.departure_date, self.departure_station, self.departure_time,
                     self.arrival_station, self.arrival_time, self.equipment,
                     self.aircraft_configuration))
