import matplotlib as mpl
import math
import numpy as np
import meteostat as mstat
import datetime

mallala_location_latitude = 34.4160
mallala_location_longitude = 138.5036

def main():
      x = datetime.datetime.now()
      print(x)
      Mallala = mstat.Point(mallala_location_latitude, mallala_location_longitude, 37)
      y = mstat.Daily(Mallala, x)
      print(y)

main()






