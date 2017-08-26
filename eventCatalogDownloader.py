import requests
import os
import sys
import numpy as np
import re
from datetime import datetime

headerstr = '''This program gathers the event information from the Global CMT website
http://www.globalcmt.org/CMTsearch.html
Monthly catalogue is available for EQs from 1994-present.
-Utpal Kumar
##############################################################'''
print(headerstr, "\n")

now = datetime.now()


# Function for downloading the catalogue
def catalogueDownload(year, month, filename):
    try:
        yrsuffix = str(year)[-2:]
        if 2005 <= year <= now.year:
            url = 'http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/NEW_MONTHLY/%s/%s%s.ndk' % (str(year), month, yrsuffix)
        elif 1994 < year <= 2004:
            url = "http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/MONTHLY/%s%s.dek" % (month, yrsuffix)
        elif year <= 1994:
            url = 'http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/jan76_dec04.dek'

        if not os.path.exists(filename):
            r = requests.get(url)
            with open(filename, "wb") as file:
                file.write(r.content)
        else:
            print("-->\tCatalogue file already exists!")
    except:
        print("ERROR downloading the data")


if __name__ == "__main__":
    yearrange = input("Enter the year/month range(1994-present)\nFormat:'yyyy/mm-yyyy/mm'\ne.g. '2003/01-2004/12': ")

    # Checking for the input format
    rex = re.compile("^[0-9]{4}/[0-9]{2}-[0-9]{4}/[0-9]{2}$")
    if not rex.match(yearrange):
        print("Please enter the correct format")
        sys.exit()

    try:
        years1 = yearrange.split("-")
        years2 = years1[0].split("/")
        years3 = years1[1].split("/")
        yearS = int(years2[0])
        monS = int(years2[1])
        yearE = int(years3[0])
        monE = int(years3[1])
        if yearS > yearE or now.year < yearE:
            sys.exit()
        elif yearS < 1976:
            print("Catalogue file is not available")
            sys.exit()
        outdir = input("Enter the path to the download directory (else Enter for current directory): ")
        if outdir == "":
            outdir = "."
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        for year in np.arange(yearS, yearE + 1):
            if year > 1994:
                # for starting year
                if year == yearS:
                    for month in months[monS - 1:]:
                        print("Downloading the catalogue for %d/%s" % (year, month))
                        filename = outdir + "/" + month + str(year)[-2:] + ".txt"
                        catalogueDownload(year, month, filename)

                # for ending year
                elif year == yearE:
                    for month in months[:monE]:
                        print("Downloading the catalogue for %d/%s" % (year, month))
                        filename = outdir + "/" + month + str(year)[-2:] + ".txt"
                        catalogueDownload(year, month, filename)
                # for other years
                else:
                    for month in months:
                        print("Downloading the catalogue for %d/%s" % (year, month))
                        filename = outdir + "/" + month + str(year)[-2:] + ".txt"
                        catalogueDownload(year, month, filename)

            else:
                print("Downloading the catalogue for 1976-2004")
                filename = outdir + "/" + 'jan76_dec04' + ".txt"
                catalogueDownload(year, 'none', filename)
    except:
        print("Please follow the proper format.")
        if yearS < 1976:
            print("Catalogue file is not available!")
        elif yearS > yearE:
            print("Starting/Ending year order doesn't seem to be correct!")
        elif now.year < yearE:
            print("Please enter available end year!")
