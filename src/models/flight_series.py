

class FlightSeries: 

    def __init__(self, flight_series_data):
        
        self.airline_designator = flight_series_data['Airline designator']
        self.flight_number = flight_series_data['Flight number']
        self.service_type = flight_series_data['Service Type']
        self.effective_date = flight_series_data['Eff']
        self.discontinued_date = flight_series_data['Dis']
        self.days_of_operation = flight_series_data['Day(s) of operation']
        self.departure_station = flight_series_data['Dept Stn']
        self.departure_time = flight_series_data['Dept time (pax)']
        self.arrival_station = flight_series_data['Arvl Stn']
        self.arrival_time = flight_series_data['Arvl time (pax)']
        self.equipment = flight_series_data['Equipment']
        self.aircraft_configuration = flight_series_data['Aircraft configuration']


    # cols_to_keep = [
    # 'Airline designator',
    # 'Flight number',
    # 'Service Type',
    # 'Eff',
    # 'Dis',
    # 'Day(s) of operation',
    # 'Dept Stn',
    # 'Dept time (pax)', 
    # 'Arvl Stn',
    # 'Arvl time (pax)',
    # 'Equipment', 
    # 'Aircraft configuration']