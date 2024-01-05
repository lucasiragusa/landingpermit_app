
import sys
from pathlib import Path

main_path = Path(__file__).resolve().parent

if str(main_path) not in sys.path:
    sys.path.append(str(main_path))

# Right now this main to be used as testbed
from models.ssim_file import SSIM_File
from models.airport import Airport
from models.flight_series_handler import FlightSeriesHandler
from models.flight_handler import FlightHandler
from lib.permit_generator import generate_document_from_flight_series
from lib.serialize_flights import serialize_flights
from lib.comparer import compare_flights, get_countries_with_changes
import time

import sys
import os
import pandas as pd
import zipfile
import io

import cProfile
from functools import wraps
from pstats import Stats, SortKey
from time import time

def profile(f):
    """A simple timer decorator"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as pr:
            result = f(*args, **kwargs)
        ps = Stats(pr)
        print("Most time spent in general:")
        ps.sort_stats(SortKey.CUMULATIVE).print_stats(10)
        print("Functions taking most time:")
        ps.sort_stats(SortKey.TIME).print_stats(10)
        return result
    return wrapper

@profile
def compute_batch(ssim_relative_path): 
         
    # Resolve Path and create SSIM_File object
    ssim_path = Path(ssim_relative_path)
    ssim_absolute_path = ssim_path.resolve()
    ssim_object = SSIM_File(str(ssim_absolute_path))

    # Declare handlers
    series_handler = FlightSeriesHandler()
    flight_handler = FlightHandler()
    
    # Create flight series from SSIM file
    series_handler.create_flight_series_from_df(ssim_object.df)

    # De-serialize the Flight series to Flight objects
    flight_list = series_handler.de_serialize_flight_series(series_handler.flight_series_collection)

    # Re-serialize the Flight objects to FlightSeries objects 
    flight_list_grouped = flight_handler.group_flights(flight_list) #First create groupings 
    serialized_flights = []
    
    for k, v in flight_list_grouped.items():
        serialized_flights.append(serialize_flights(v))

    # Flatten the resulting list of lists of FlightSeries objects
    serialized_flights = [item for sublist in serialized_flights for item in sublist]

    # Get all unique countries from the SSIM file
    unique_countries = series_handler.get_unique_countries(serialized_flights)

    # print (serialized_flights)

    # Filter by a specific country and print results.  
    for country_code in unique_countries:
        print (f'Creating permit for: {country_code}')
        
        start_time = time.time()  # Start timing
        generate_document_from_flight_series(country_code, serialized_flights, 'FlySample', 'Luca Siragusa', series_handler)
        end_time = time.time()  # End timing

        duration = end_time - start_time
        print(f'Time taken for {country_code}: {duration:.2f} seconds\n')

def test_batch_streamlit(uploaded_file): 
         
    # Get the SSIM file path from the uploaded file
    ssim_object = SSIM_File(str(uploaded_file))

    # Declare handlers
    series_handler = FlightSeriesHandler()
    flight_handler = FlightHandler()
    
    # Create flight series from SSIM file
    series_handler.create_flight_series_from_df(ssim_object.df)

    # De-serialize the Flight series to Flight objects
    flight_list = series_handler.de_serialize_flight_series(series_handler.flight_series_collection)

    # Re-serialize the Flight objects to FlightSeries objects 
    flight_list_grouped = flight_handler.group_flights(flight_list) #First create groupings 
    serialized_flights = []
    
    for k, v in flight_list_grouped.items():
        serialized_flights.append(serialize_flights(v))

    # Flatten the resulting list of lists of FlightSeries objects
    serialized_flights = [item for sublist in serialized_flights for item in sublist]

    # Get all unique countries from the SSIM file
    unique_countries = series_handler.get_unique_countries(serialized_flights)

    # print (serialized_flights)
    
    # Output to a ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for country_code in unique_countries:
            # Assuming generate_document_from_flight_series creates files, save them to the zip
            file_path = generate_document_from_flight_series(country_code, serialized_flights, 'FlySample', 'Luca Siragusa', series_handler)
            zip_file.write(file_path, arcname=Path(file_path).name)

    zip_buffer.seek(0)
    return zip_buffer

def test_comparative(): 
    # Get the SSIM file path from the command line argument
    base_ssim_relative_path = sys.argv[1]
    alt_ssim_relative_path = sys.argv[2]

    # Resolve Path and create SSIM_File object
    
    # For the base SSIM file
    base_ssim_path = Path(base_ssim_relative_path)
    base_ssim_absolute_path = base_ssim_path.resolve()
    base_ssim_object = SSIM_File(str(base_ssim_absolute_path))
    
    # For the alt SSIM file 
    alt_ssim_path = Path(alt_ssim_relative_path)
    alt_ssim_absolute_path = alt_ssim_path.resolve()
    alt_ssim_object = SSIM_File(str(alt_ssim_absolute_path))

    # De-serialize flights from SSIM files
    base_flight_list = base_ssim_object.de_serialize()
    alt_flight_list = alt_ssim_object.de_serialize()
    
    # Re-serialize flights for base and alt
    flight_handler = FlightHandler()
    series_handler = FlightSeriesHandler()
    
    base_flight_list_grouped = flight_handler.group_flights(base_flight_list) #First create groupings
    base_serialized_flights = []
    
    for k, v in base_flight_list_grouped.items():
        base_serialized_flights.append(serialize_flights(v))
        
    base_serialized_flights = [item for sublist in base_serialized_flights for item in sublist]
    
    alt_flight_list_grouped = flight_handler.group_flights(alt_flight_list) #First create groupings
    alt_serialized_flights = []
    
    for k, v in alt_flight_list_grouped.items():
        alt_serialized_flights.append(serialize_flights(v))
        
    alt_serialized_flights = [item for sublist in alt_serialized_flights for item in sublist]
    
    # Compare flights
    flight_comparison_dict = compare_flights(base_flight_list, alt_flight_list)
    
    # Get countries with changes
    countries_with_changes = get_countries_with_changes(flight_comparison_dict['modified_flights'])
        
    # Print countries with changes
    print(f'Countries with changes: {countries_with_changes}')
    
    
    ###########
    # THIS CAN BE RE-WRITTEN TO SHOW BOTH OLD AND MODIFIED FLIGHTS
    ###########
    
    # Filter by a specific country and print results.  
    for country_code in countries_with_changes:
        print (f'Creating permit for: {country_code}')
        
        start_time = time.time()  # Start timing
        generate_document_from_flight_series(country_code, alt_serialized_flights, 'FlySample', 'Luca Siragusa', series_handler)
        end_time = time.time()  # End timing

        duration = end_time - start_time
        print(f'Time taken for {country_code}: {duration:.2f} seconds\n')
    



if __name__ == '__main__':

    # Get the SSIM file path from the command line argument
    ssim_relative_path = sys.argv[1]

    start_time = time.time()  # Record the start time

    compute_batch(ssim_relative_path=ssim_relative_path)

    end_time = time.time()  # Record the end time
    duration = end_time - start_time  # Calculate the duration

    print(f"Execution time: {duration} seconds")
