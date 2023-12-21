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
    """
    Compare two sets of flights and categorize them based on changes.

    Parameters:
    - base_flights (set): A set of Flight objects representing the base flights.
    - alt_flights (set): A set of Flight objects representing the alternative flights.

    Returns:
    - dict: A dictionary with sets under 'old_flights', 'new_flights', and 'modified_flights' keys.
    """
    
    flight_changes = {
        'old_flights': set(),
        'new_flights': set(),
        'modified_flights': set()
    }

    # Identify new and deleted flights using set operations
    new_flights = alt_flights - base_flights
    deleted_flights = base_flights - alt_flights

    # Handle new and deleted flights
    for flight in new_flights:
        flight_clone = deepcopy(flight)
        flight_clone.change_status = 'NEW'
        flight_changes['new_flights'].add(flight_clone)

    for flight in deleted_flights:
        flight_clone = deepcopy(flight)
        flight_clone.change_status = 'CNL'
        flight_changes['old_flights'].add(flight_clone)

    # Check for modified flights
    common_flights = base_flights & alt_flights
    for flight in common_flights:
        alt_flight = next(f for f in alt_flights if f.unique_id == flight.unique_id)

        if flight != alt_flight:  # There's a modification
            flight_clone = deepcopy(flight)

            if flight.departure_time != alt_flight.departure_time or flight.arrival_time != alt_flight.arrival_time:
                flight_clone.change_status = 'TIM'
            elif flight.equipment != alt_flight.equipment:
                flight_clone.change_status = 'EQP'

            if flight_clone.change_status:
                flight_changes['modified_flights'].add(flight_clone)

    return flight_changes



# To Test this, we will be reading an SSIM Files, which produces FLight_series 
# We will de-serialize the series into flights objects and compare them


if __name__ == '__main__':
    
    import time 
    import json
    
    start_time = time.time()  # Start timing

    # Create a flight series handler
    base_dir = Path(__file__).resolve().parent.parent.parent
    base_ssim_path = base_dir / 'data' / 'ssim' / 'EY_SSIM_base_compare.ssim'
    alt_ssim_path = base_dir / 'data' / 'ssim' / 'EY_SSIM_alt_compare.ssim'
    
    base_set = de_serialize(base_ssim_path)
    alt_set = de_serialize(alt_ssim_path)
    
    result = compare_flights(base_set, alt_set)

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
