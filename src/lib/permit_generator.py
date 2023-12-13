import sys
import os
import pandas as pd

# TODO: install lib as package instead
# This will get the path to the parent directory of the current directory (i.e., landingpermit_app)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import flight_series_handler, airport_data_loader, airport, flight_series, ssim_file


from docx import Document
from docx.shared import Inches


def generate_document(country, ssim_file, airline_name, contact_person, handler): # TODO: add type hints?
    # TODO: add docstring
    start_date = ssim_file.start_date
    end_date = ssim_file.end_date

    # Initialize python docx document
    doc = Document()

    # Add the static content
    doc.add_heading('Request for Landing Permit', 0)

    # Add a first paragraph with sample content
    doc.add_paragraph(
        ("Dear Sir/Madam,\n\n"
         "I am writing to request a landing permit for {country} "
         "for the period {start_date} to {end_date}.\n\n"
         "{airline_name} is a scheduled airline operating flights to {country}.\n\n"
         "We are planning to operate the following flights to {country}:").format(
             country=country, 
             start_date=start_date.strftime('%d %B %Y'), 
             end_date=end_date.strftime('%d %B %Y'), 
             airline_name=airline_name)
    )

    # Filter flight series by country using the handler
    flight_series = handler.filter_by_country(country)

    # Convert filtered flight series to DataFrame (assuming you have a method in FlightSeries object to return its data as a dict)
    data_dicts = [fs.to_dict() for fs in flight_series]
    df = pd.DataFrame(data_dicts)

    # Add a table with the flight series
    t = doc.add_table(df.shape[0] + 1, df.shape[1])
    
    # Add column headers
    for j, column in enumerate(df.columns):
        t.cell(0, j).text = column
        
    # Populate rest of the table with the flight series data
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            t.cell(i + 1, j).text = str(df.values[i, j])

    # Add a line break after the table
    doc.add_paragraph("\n")

    # Add signature paragraph
    doc.add_paragraph(f'Sincerely, {contact_person}')

    # Ensure directory structure exists before saving
    base_directory = os.path.join(os.getcwd(), "permits_output")
    country_directory = os.path.join(base_directory, country)
    
    if not os.path.exists(country_directory):
        os.makedirs(country_directory)
        
    doc.save(os.path.join(country_directory, f'landing_permit_{country}.docx'))
