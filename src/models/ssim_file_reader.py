import pendulum
import pandas as pd

class SSIMFileReader:

    def __init__(self, ssim_file_path):
        self.ssim_file_path = ssim_file_path

    def get_attributes(self):
        '''
        This function takes an SSIM file and returns a dictionary with the main attributes of the file.
        For example, it tells if the file is in local or UTC mode, the start and end date of the file in local and utc, etc
        The idea of this function is that it will be used to create a SSIMFile object 
        '''
        
        with open(self.ssim_file_path, 'r') as file:
            for line in file:
                if line.startswith('2'):
                    self.timezone_mode = 'local' if line[1] == 'L' else 'UTC' if line[1] == 'U' else None
                    
                    start_date_str = line[14:21].title()  # Convert to format with first letter capital
                    self.start_date = pendulum.from_format(start_date_str, "DDMMMYY")

                    end_date_str = line[21:28].title()  # Convert to format with first letter capital
                    self.end_date = pendulum.from_format(end_date_str, "DDMMMYY")

                    try:
                        exported_date_str = line[28:35].title()  # Convert to format with first letter capital
                        self.exported_date = pendulum.from_format(exported_date_str, "DDMMMYY")
                    except:
                        self.exported_date = None
                    
                    # Once we find and process the line starting with '2', we can break out of the loop
                    break
        return {
        'timezone_mode': self.timezone_mode,
        'start_date': self.start_date,
        'end_date': self.end_date,
        'exported_date': self.exported_date
        }

    def get_dataframe(self, filename, col_length, col_headers, cols_to_keep):

        """Parses a fixed-width file (SSIM) and returns a filtered dataframe based on given specifications.
    
        This function will filter out rows specific to flights (where Record type is 3) and also 
        apply specific transformations to columns 'Arvl time (pax)' and 'Flight number'.
        It then stores the resultant dataframe as an attribute for the instance.
        
        Parameters:
        - filename (str): The path to the SSIM file to be read.
        - col_length (list of tuple): A list specifying the start and end position of each column.
        - col_headers (list of str): A list containing names for each column.
        - cols_to_keep (list of str): Columns that are to be retained in the final dataframe.
        
        Returns:
        None. But it updates the instance's `df` attribute with the processed dataframe. """

        df = pd.read_fwf(filename, colspecs=col_length, header=None, names=col_headers)
        # Filter rows for flights
        df = df[df['Record type'] == 3]
        df = df[cols_to_keep]
        df['Arvl time (pax)'] = df['Arvl time (pax)'].apply(lambda x: str(int(x)).zfill(4))
        df['Flight number'] = df.apply(lambda x: x['Airline designator'] + '  ' + str(x['Flight number']).zfill(4), axis=1)
        # df.drop(columns=['Airline designator'], inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df

    def export_df (self, filename):
        self.df.to_csv(filename, index=False)