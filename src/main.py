
# Right now this main to be used as testbed
from models.ssim_file import SSIM_File
import sys
import os
import pandas as pd
import pendulum

sys.path.append(os.path.dirname(os.path.abspath(__file__)))




def main(): 
    
    ssim = sys.argv[1]

    ssim_object = SSIM_File(ssim)

    for season in ssim_object.iata_seasons: 
        print (season.name)

if __name__ == '__main__':
    main()

