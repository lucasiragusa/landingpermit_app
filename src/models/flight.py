# TODO: What shall this be about?
# A flight series is a series of flights that have the same exact characteristics 
# (same origin, destination, flight number, departure time, arrival time, season etc.)
# But fundamentally it is made up by individual flights, this class is supposed to represent individual flights 
# It will be useful in the part where we compare the base ssim with the alt ssim and output only the flights that changed

from models.airport import airport_data, Airport
import pendulum


class Flight:
    """
    Represents a single flight. This class has similar attributes to the FlightSeries class,
    but instead of a series of flights, it represents a single flight with a specific departure date.

    Attributes:
        airline_designator (str): The IATA Designator of the Operating Airline.
        flight_number (str): The flight number.
        service_type (str): SSIM-compliant Service type indicating the type of flight (e.g. scheduled pax, cargo, etc.)
        departure_date (str): The departure date of the flight.
        departure_station (Airport): The airport from which the flight departs.
        departure_time (str): The scheduled departure time of the flight.
        arrival_station (Airport): The airport at which the flight arrives.
        arrival_time (str): The scheduled arrival time of the flight.
        equipment (str): Details about the flight's equipment.
        aircraft_configuration (str): Configuration of the aircraft used in the flight.
    """

    def __init__(self, flight_data):
        self.airline_designator = flight_data['Airline designator']
        self.flight_number = flight_data['Flight number']
        self.service_type = flight_data['Service Type']
        self.departure_date = flight_data['Departure Date']
        self.departure_station = Airport(flight_data['Dept Stn'])
        self.departure_time = flight_data['Dept time (pax)']
        self.arrival_station = Airport(flight_data['Arvl Stn'])
        self.arrival_time = flight_data['Arvl time (pax)']
        self.equipment = flight_data['Equipment']
        self.aircraft_configuration = flight_data['Aircraft configuration']
        self.isocalendar = pendulum.from_format(self.departure_date, 'DDMMMYY').isocalendar()
        self.year = self.isocalendar[0]
        self.isoweek = self.isocalendar[1]
        self.weekday = self.isocalendar[2]
        self.week_signature = str(self.year) + '_' + str(self.isoweek).zfill(2)


    def _repr__(self):
        return f'{self.flight_number} {self.departure_date} {self.departure_time} {self.arrival_time} ({self.week_signature}) Weekday: {self.weekday}'

    def __str__(self) -> str:
        return f'{self.flight_number} {self.departure_date} {self.departure_time} {self.arrival_time} ({self.week_signature}) Weekday: {self.weekday}'