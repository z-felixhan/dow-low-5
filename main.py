import components as c
import time

start_time = time.time()

dowURL = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
baseURL = "https://www.marketwatch.com/investing/stock/"

c.dl5MW(baseURL, c.stocksWiki(dowURL))

elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
print("Elapsed time: " + elapsed_time)
