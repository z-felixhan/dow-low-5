import Components as c
import time

start_time = time.time()

dowURL = "https://ca.finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI"
baseURL = "https://ca.finance.yahoo.com/quote/"
statsPath = "/key-statistics"

stocks = c.stocks(dowURL)
stocksCurrentPrice = c.currentPrice(baseURL, stocks)
stocksDividend = c.dividend(baseURL, statsPath, stocks)
merged = c.merge(stocks, stocksCurrentPrice, stocksDividend)
dl5 = c.dl5(merged)

print("The below is the DOW Low 5 in the format of [STOCK, CURRENT PRICE, TRAILING DIVIDEND]:")
print(dl5)

elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
print("Elapsed time: " + elapsed_time)