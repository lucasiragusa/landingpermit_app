# TODO: what shall this be about?

from pathlib import Path
import pendulum
import pandas as pd
import sys
from pathlib import Path
from copy import deepcopy

# Add the project directory to Python's module search path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from models.flight import Flight
from models.airport import Airport
from models.de_serialize import de_serialize


def compare_flights(base_flights, alt_flights):
    flight_changes = {
        'base_flights': set(),
        'alt_flights': set(),
        'modified_flights': set()
    }
    
    flight_changes['base_flights'] = base_flights
    flight_changes['alt_flights'] = alt_flights

    # Create mappings of flights by unique_id
    base_flights_mapping = {flight.unique_id: flight for flight in base_flights}
    alt_flights_mapping = {flight.unique_id: flight for flight in alt_flights}

    # Identify flights only in base or alt flights
    base_only_ids = set(base_flights_mapping.keys()) - set(alt_flights_mapping.keys())
    alt_only_ids = set(alt_flights_mapping.keys()) - set(base_flights_mapping.keys())

    # Mark base-only flights as cancelled
    for flight_id in base_only_ids:
        flight_clone = deepcopy(base_flights_mapping[flight_id])
        flight_clone.change_status = 'CNL'
        flight_changes['modified_flights'].add(flight_clone)

    # Mark alt-only flights as new
    for flight_id in alt_only_ids:
        flight_clone = deepcopy(alt_flights_mapping[flight_id])
        flight_clone.change_status = 'NEW'
        flight_changes['modified_flights'].add(flight_clone)

    # Check for changes other than cancellation or new 
    for base_id, base_flight in base_flights_mapping.items():
        if base_id in alt_flights_mapping:
            alt_flight = alt_flights_mapping[base_id]

            if base_flight != alt_flight:  # There's a modification
                flight_clone = deepcopy(base_flight)

                if base_flight.departure_time != alt_flight.departure_time or base_flight.arrival_time != alt_flight.arrival_time:
                    flight_clone.change_status = 'TIM'
                elif base_flight.equipment != alt_flight.equipment:
                    flight_clone.change_status = 'EQP'
                # Otherwise if anything else changed, mark as 'RPL'

                if flight_clone.change_status:
                    flight_changes['modified_flights'].add(flight_clone)

    return flight_changes

def get_countries_with_changes(modified_flights):
    """
    Extracts a unique list of departure and arrival countries from modified flights.

    Args:
    modified_flights (set of Flight objects): A set of modified Flight objects.

    Returns:
    list: A unique list of all departure and arrival countries from modified flights.
    """
    countries = set()

    for flight in modified_flights:
        countries.add(flight.departure_country)
        countries.add(flight.arrival_country)

    return list(countries)



# To Test this, we will be reading an SSIM Files, which produces FLight_series 
# We will de-serialize the series into flights objects and compare them


if __name__ == '__main__':
    
    import time 
    import json
    from models.ssim_file import SSIM_File
    
    start_time = time.time()  # Start timing

    # Create a flight series handler
    base_dir = Path(__file__).resolve().parent.parent.parent
    base_ssim_path = base_dir / 'data' / 'ssim' / 'EY_SSIM_base_compare.ssim'
    alt_ssim_path = base_dir / 'data' / 'ssim' / 'EY_SSIM_alt_compare.ssim'

    base_object = SSIM_File(base_ssim_path)
    alt_object = SSIM_File(alt_ssim_path)
    
    base_set = de_serialize(base_ssim_path)
    alt_set = de_serialize(alt_ssim_path)
    
    result = compare_flights(base_set, alt_set)
    
    for flight in result['modified_flights']:
        print(f'{flight} {flight.change_status}')

    end_time = time.time()  # End timing
    
    elapsed_time = end_time - start_time
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")

    # Convert Flight objects to their string representations
    for key in result:
        result[key] = [str(flight) for flight in result[key]]

    # Writing result to a file
    result_file_path = base_dir / 'compare_testing.json'
    with open(result_file_path, 'w') as file:
        json.dump(result, file, indent=4)


    print(f"Results written to {result_file_path}")