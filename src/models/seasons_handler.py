import pendulum
from models.iata_season import IATA_Season


class DateSeasonHandler:

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    # Helper function to determine the season of a given date

    # TODO: isn't there already a built-in function for this? 
    # Not to my knowledge, this concept of Season is specific to IATA, Summer season starts on the last Sunday of March and ends on the last Sunday of October
    # If there is a built-in function for this, it would be great to use it instead
    # I also thought a good byproduct of this work would be to open-source certain functions like this for other aviation people to use
    
    def determine_season(self, date):
        summer_start = pendulum.datetime(date.year, 3, 31, 0, 0, 0).last_of('month', day_of_week=pendulum.SUNDAY)
        winter_start = pendulum.datetime(date.year, 10, 31, 0, 0, 0).last_of('month', day_of_week=pendulum.SUNDAY)
        
        if summer_start <= date < winter_start:
            return 'S' + str(date.year)[2:]
        else:
            if date < summer_start:
                return 'W' + str(date.year - 1)[2:]
            else:
                return 'W' + str(date.year)[2:]
            
    
    def get_iata_seasons(self):
        seasons = []
        
        # Identify the season of the start and end dates
        start_season = self.determine_season(self.start_date)
        end_season = self.determine_season(self.end_date)

        # Now fill in the seasons in between
        current_season = start_season
        while current_season != end_season:
            seasons.append(current_season)

            # Move to the next season
            if 'S' in current_season:
                current_season = 'W' + current_season[1:]
            else:
                year = int(current_season[1:]) + 1
                current_season = 'S' + str(year).zfill(2)
        
        # Add the end season and return
        seasons.append(end_season)

        return [IATA_Season(season) for season in seasons]