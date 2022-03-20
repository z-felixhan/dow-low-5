# DOW Low 5

Calculates the Dow Jones Industrial Average (DOW) Low 5 by retrieving the ticker for each component from Wikipedia and grabbing its associated dividend yield and price from Market Watch.

The DOW Low 5 takes the list of the top 10 highest paying dividend stocks from the DOW, and trims it down to the 5 cheapest.

Has dependencies on urllib.request and BeautifulSoup modules in Python 3.
