
# Right now this main to be used as testbed
from models.ssim_file import SSIM_File
from models.airport import Airport
from models.flight_series_handler import FlightSeriesHandler
from models.flight_handler import FlightHandler
from lib.permit_generator import generate_document
from lib.serialize_flights import serialize_flights
import time

import sys
import os
import pandas as pd
import pendulum

# TODO: install as package instead
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve()))


def main(): 
    
    print (f'Main executing.')
     
    # Get the SSIM file path from the command line argument
    ssim_relative_path = sys.argv[1]

    # Convert the relative path string to a Path object
    ssim_path = Path(ssim_relative_path)

    # Resolve the absolute path
    ssim_absolute_path = ssim_path.resolve()

    print(f'SSIM path: {ssim_absolute_path}')

    ssim_object = SSIM_File(str(ssim_absolute_path))

    series_handler = FlightSeriesHandler()
    flight_handler = FlightHandler()
    # handler.create_flight_series_from_df(ssim_object.df)

    # # If you want to print all unique countries present in the flight series
    # unique_countries = handler.get_unique_countries()

    # # Filter by a specific country and print results.  
    # for country_code in unique_countries:
    #     print (f'Creating permit for: {country_code}')
        
    #     start_time = time.time()  # Start timing
    #     generate_document(country_code, ssim_object, 'FlySample', 'Luca Siragusa', handler)
    #     end_time = time.time()  # End timing

    #     duration = end_time - start_time
    #     print(f'Time taken for {country_code}: {duration:.2f} seconds\n')
    
    # Test ssim read to df
    ssim_object.df.to_csv('../tests/ssim_df.csv', index=False)
        
    # test de-serializing ssim before 
    
    flight_list = ssim_object.de_serialize()
    
    flight_list_grouped = flight_handler.group_flights(flight_list)
    
    print (f'Flights list_grouped: {flight_list_grouped}')
    
    for flight_group, flight in flight_list_grouped.items():
        print(flight_group)
        for f in flight:
            print(f)
        print('\n')


def main_2(): 
    output_file_path = '../tests/output.txt'
    start_time = time.time() 

    with open(output_file_path, 'w') as file:
        file.write('Main executing.\n')
        file.flush()
        
        ssim_relative_path = sys.argv[1]
        ssim_path = Path(ssim_relative_path)
        ssim_absolute_path = ssim_path.resolve()
        
        file.write(f'SSIM path: {ssim_absolute_path}\n')
        file.flush()

        # Assuming SSIM_File, FlightSeriesHandler, FlightHandler are defined elsewhere
        ssim_object = SSIM_File(str(ssim_absolute_path))

        series_handler = FlightSeriesHandler()
        flight_handler = FlightHandler()

        # Your existing code for handling SSIM file and flights...

        ssim_object.df.to_csv('../tests/ssim_df.csv', index=False)

        flight_list = ssim_object.de_serialize()
        flight_list_grouped = flight_handler.group_flights(flight_list)
        
        # file.write(f'Flights list_grouped: {flight_list_grouped}\n')     
        # file.flush()
        
        for flight_group, flights in flight_list_grouped.items():
                    
            file.write(f'flight group: \n')
            file.write(f'{flight_group}\n')
            
            file.flush()
            
            file.write(f'Serialized flights: \n')
            serialized_flights = serialize_flights(flights)
            file.write(f'\n')
            
            for series in serialized_flights:
                file.write(f'{series}\n')
            file.write(f'\n')
            
            file.write(f'-----------------------------------\n')
            
            file.flush()
            
            end_time = time.time()  # End the timer
            file.flush()

        elapsed_time = end_time - start_time
        print (f'Executed in: {elapsed_time} seconds')

            # file.write(f'Flights: \n')
            
            # for f in flights:
            #     file.write(f'{f}\n')
            # file.write('\n')
            # file.flush()
            
            

if __name__ == '__main__': 
    main_2()

