import Components as c

dowURL = "https://ca.finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI"
baseURL = "https://ca.finance.yahoo.com/quote/"
statsPath = "/key-statistics"

stocks = c.stocks(dowURL)
stocksCurrentPrice = c.currentPrice(baseURL, stocks)
stocksDividend = c.dividend(baseURL, statsPath, stocks)

print(stocks)
print(stocksCurrentPrice)
print(stocksDividend)