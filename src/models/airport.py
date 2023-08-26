from models.airport_data_loader import airport_data

class Airport: 
        
    def __init__(self, iata_code):
        self.iata_code = iata_code
        self.icao_code = airport_data[iata_code]['ICAO code']
        self.airport_name = airport_data[iata_code]['Airport name']
        self.latitude = airport_data[iata_code]['Latitude']
        self.longitude = airport_data[iata_code]['Longitude']
        self.iso_country = airport_data[iata_code]['ISO country']
        self.iso_region = airport_data[iata_code]['ISO region']
        self.city = airport_data[iata_code]['municipality']
        self.country_name = airport_data[iata_code]['Country name']
        self.timezone = airport_data[iata_code]['Timezone']

    def __repr__(self):
        return str(airport_data[self.iata_code])
    
