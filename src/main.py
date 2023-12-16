
# Right now this main to be used as testbed
from models.ssim_file import SSIM_File
from models.airport import Airport
from models.flight_series_handler import FlightSeriesHandler
from lib.permit_generator import generate_document
import time #debug

import sys
import os
import pandas as pd
import pendulum

# TODO: install as package instead
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve()))


def main(): 
    import numpy as np 

    ssim = sys.argv[1]
    ssim_object = SSIM_File(ssim)

    handler = FlightSeriesHandler()
    handler.create_flight_series_from_df(ssim_object.df)

    # If you want to print all unique countries present in the flight series
    unique_countries = handler.get_unique_countries()

    # Filter by a specific country and print results.
    for country_code in unique_countries:
        print (f'Creating permit for: {country_code}')
        
        start_time = time.time()  # Start timing
        generate_document(country_code, ssim_object, 'FlySample', 'Luca Siragusa', handler)
        end_time = time.time()  # End timing

        duration = end_time - start_time
        print(f'Time taken for {country_code}: {duration:.2f} seconds\n')

if __name__ == '__main__':
    main()
