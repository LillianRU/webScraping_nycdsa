import pandas as pd
from cleaning import *


airbnb = readData()

print(cleanDF(airbnb).columns)

print(airbnb.columns)