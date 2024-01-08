import pandas as pd
from pathlib import Path


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
    
    def __str__(self) -> str:
        return self.iata_code
        pass
    
    def __eq__(self, other):
        if not isinstance(other, Airport):
            return False

        return (self.iata_code == other.iata_code and
                self.icao_code == other.icao_code and
                self.airport_name == other.airport_name and
                self.latitude == other.latitude and
                self.longitude == other.longitude and
                self.iso_country == other.iso_country and
                self.iso_region == other.iso_region and
                self.city == other.city and
                self.country_name == other.country_name and
                self.timezone == other.timezone)

    def __hash__(self):
        return hash((self.iata_code, self.icao_code, self.airport_name,
                     self.latitude, self.longitude, self.iso_country,
                     self.iso_region, self.city, self.country_name,
                     self.timezone))


# Calculate the path relative to the current file
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent.parent  # Navigate up to the project root
data_file_path = project_root / 'data' / 'industry' / 'airport_data.pkl'  # Construct the path to the data file

# Load the data
airport_data = pd.read_pickle(data_file_path)

