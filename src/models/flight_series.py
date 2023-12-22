from models.airport import airport_data
from models.airport import Airport

class FlightSeries: 

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
        #Add number of Flights

    def __repr__(self):
        return f"{self.airline_designator} {self.flight_number}: {self.departure_station}-{self.arrival_station} ({self.effective_date}-{self.discontinued_date})"
    
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