import pendulum 

def parse_date(date_str, date_format = 'DDMMMYY'):
    """
    Parses a date string in a specific format to a datetime object.

    Args:
        date_str (str): Date string in '01May23' format.

    Returns:
        datetime.date: Parsed date.
    """
    return pendulum.from_format(date_str, date_format)

# Function that returns the week signature of a date

def get_week_signature(date_str, date_format = 'DDMMMYY'):
    """
    Returns the week signature of a date.

    Args:
        date_str (str): Date string in '01May23' format.

    Returns:
        str: Week signature of the date.
    """
    date = parse_date(date_str, date_format)
    return str(date.year) + '_' + str(date.isocalendar()[1])

# Function that returns the weekday of a date

def get_weekday(date_obj):
    """
    Returns the weekday of a date.

    Args:
        date_str (str): Date string in '01May23' format.

    Returns:
        int: Weekday of the date.
    """
    return date_obj.isocalendar()[2]

# Function that returns the year of a date 

def get_year(date_str, date_format = 'DDMMMYY'):
    """
    Returns the year of a date.

    Args:
        date_str (str): Date string in '01May23' format.

    Returns:
        int: Year of the date.
    """
    date = parse_date(date_str, date_format)
    return date.year

# Function that returns the week number of a date

def get_week_number(date_str, date_format = 'DDMMMYY'):
    """
    Returns the week number of a date.

    Args:
        date_str (str): Date string in '01May23' format.

    Returns:
        int: Week number of the date.
    """
    date = parse_date(date_str, date_format)
    return date.isocalendar()[1]

# Function that returns number of days between two dates (incl first and last)

def get_date_range(start_date_str, end_date_str, date_format = 'DDMMMYY'):
    """
    Returns the number of days between two dates (including first and last).

    Args:
        start_date_str (str): Date string in '01May23' format.
        end_date_str (str): Date string in '01May23' format.

    Returns:
        int: Number of days between the two dates.
    """
    start_date = parse_date(start_date_str, date_format)
    end_date = parse_date(end_date_str, date_format)
    return (end_date - start_date).days + 1


def pendulum_to_string(date_obj, date_format = 'DDMMMYY'):
    """
    Formats a date object into a specific string format.

    Args:
        date_obj (datetime.date or pendulum.DateTime): Date object.
        date_format (str): The format string, default is 'DDMMMYY'.

    Returns:
        str: Formatted date string.
    """
    return date_obj.format(date_format)


def reformat_date_signature(date_str):
    """
    Converts a date string from '01JAN23' format to '01Jan23' using string manipulation.

    Args:
        date_str (str): Date string in '01JAN23' format.

    Returns:
        str: Reformatted date string in '01Jan23' format.

    Raises:
        ValueError: If the date_str does not match the expected format.
    """
    # Check if date_str is 7 characters long
    if len(date_str) != 7:
        raise ValueError(f"{date_str} does not match format: length is not 7 characters")

    # Extract day, month, and year parts
    day = date_str[:2]
    month = date_str[2:5]
    year = date_str[5:]

    # Validate day and year are numeric
    if not (day.isdigit() and year.isdigit()):
        raise ValueError(f"{date_str} does not match format: day and year are not numeric")

    # List of valid month abbreviations
    valid_months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    # Validate month
    if month.upper() not in valid_months:
        raise ValueError(f"{date_str} does not match format: month is not valid")

    # Reformat month to title case
    month = month.title()

    # Combine and return the reformatted date string
    return day + month + year



# if __name__ == '__main__': 
#     reformat_date_signature('01JAN23')