import pendulum

class IATA_Season: 

    def __init__(self, iata_season):
        self.name = iata_season
        self.start_date, self.end_date = self._calculate_dates(iata_season)

    def _calculate_dates(self, iata_season):
        year = 2000 + int(iata_season[1:3])  # Convert to four-digit year

        if iata_season[0] == "S":
            start_date = pendulum.datetime(year, 3, 31, 0, 0, 0).last_of('month', day_of_week=pendulum.SUNDAY)
            winter_start = pendulum.datetime(year, 10, 31, 0, 0, 0).last_of('month', day_of_week=pendulum.SUNDAY)
            end_date = winter_start.subtract(days=1)
        else:
            start_date = pendulum.datetime(year, 10, 31, 0, 0, 0).last_of('month', day_of_week=pendulum.SUNDAY)
            next_year_summer_start = pendulum.datetime(year+1, 3, 31, 0, 0, 0).last_of('month', day_of_week=pendulum.SUNDAY)
            end_date = next_year_summer_start.subtract(days=1)

        return start_date, end_date

    def __repr__(self):
        return f"{self.name}: {self.start_date} to {self.end_date}"


# Test code
# if __name__ == '__main__':
#     import sys
#     import time
    
#     ssim = sys.argv[1]

#     start_time = time.time()  # Start the timer

#     ssim_object = SSIM_File(ssim)

#     print(ssim_object.start_date)
#     print(ssim_object.end_date)

#     # print(ssim_object.df.head())

#     elapsed_time = time.time() - start_time  # Calculate elapsed time

#     print(f"\nTime taken to execute read_ssim: {elapsed_time:.2f} seconds")