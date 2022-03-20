from bs4 import BeautifulSoup
from operator import itemgetter
from urllib.request import urlopen


def stocks(url):
    ''' (string) -> list

    Takes the Yahoo URL to components of an index and grabs the individual stock names.

    >>>stocks("https://ca.finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI")
    ['DIS', 'WBA', 'IBM', 'MMM', 'PG', 'XOM', 'VZ', 'AAPL', 'CVX', 'MRK', 'JNJ', 'AXP', 'UTX', 'CAT', 'INTC', 'HD', 'V', 'WMT', 'KO', 'PFE', 'NKE', 'TRV', 'MCD', 'GS', 'MSFT', 'JPM', 'CSCO', 'DOW', 'UNH', 'BA']

    >>>stocks("https://ca.finance.yahoo.com/quote/%5EIXIC/components?p=%5EIXIC")
    ['FNKO', 'SLAB', 'FEYE', 'FARO', 'TSLA', 'CVCY', 'FNLC', 'IBKC', 'SPHS', 'NVCR', 'FRTA', 'EXAS', 'CMRX', 'ATEC', 'IFRX', 'AGLE', 'CVCO', 'OPTT', 'NVCN', 'NMRK', 'POPE', 'TBIO', 'SCON', 'KLXE', 'FRSX', 'FNJN', 'AKTX', 'FARM', 'TWST', 'SCOR']
    '''

    html = urlopen(url)
    titles = []
    soup = BeautifulSoup(html, "lxml")

    #Finds the <a> tags in the table that comprises the components of the index and grabs the title attribute
    for a in soup.tbody.find_all('a'):
        titles.append(a.get('title'))

    return titles


def currentPrice(url, stocks):
    ''' (string, list) -> list

    Returns a list of current prices for each stock respectively.

    >>>currentPrice("https://ca.finance.yahoo.com/quote/", ["MSFT"])
    ['137.78']
    >>>currentPrice("https://ca.finance.yahoo.com/quote/", ["WMT", "INTL", "FEYE"])
    ['111.91', '38.74', '13.57']
    '''

    result = []

    #Takes each stock and gets their current price
    for item in stocks:
        html = urlopen(url + item)
        soup = BeautifulSoup(html, "lxml")

        #NOTE: Another way is to grab the location of "At close" text and find the stock price from there
        result.append(soup.select_one('span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\)').text)

    return result


def dividend(url, path, stocks):
    ''' (string, string, list) -> list

    Returns the trailing dividend yield of each stock respectively.

    >>>dividend("https://ca.finance.yahoo.com/quote/", "/key-statistics", ["MSFT"])
    ['1.33%']
    >>>divident("https://ca.finance.yahoo.com/quote/", "/key-statistics", ["WMT", "INTL", "FEYE"])
    ['1.87%', 'N/A', 'N/A']
    '''

    result = []

    #Takes each stock and gets their trailing annual dividend yield
    for item in stocks:
        html = urlopen(url + item + path)
        soup = BeautifulSoup(html, "lxml")

        result.append(soup.find(text="Trailing Annual Dividend Yield").parent.parent.nextSibling.text)

    return result


def merge(listOne, listTwo, listThree):
    ''' (list, list, list) -> list

    Merges three lists.

    >>>merge(['PG'], ['118.71'], ['2.43%'])
    [['PG', '118.71', '2.43%']]
    >>>merge(['UNH', 'VZ', 'CVX'], ['231.22' '56.27' '116.56'], ['1.62%', '4.24%', '3.92%'])
    [['UNH', '231.22', '1.62%'], ['VZ', '56.27', '4.24%'], ['CVX', '116.56', '3.92%']]
    '''
    
    length = len(listOne)
    result = []

    for i in range(length):
        result.insert(i, [listOne[i], float(listTwo[i]), listThree[i]])

    return result


def dl5(raw):
    ''' (list) -> (list)

    Returns the DOW Low 5 stocks.

    >>>dl5([['BA', 356.01, '2.12%'], ['WMT', 110.83, '1.88%'], ['UNH', 230.66, '1.62%'], ['KO', 53.74, '2.90%'], ['VZ', 55.92, '4.24%'], ['HD', 217.47, '2.31%'], ['PG', 117.32, '2.43%'], ['MRK', 84.94, '2.38%'], ['TRV', 144.73, '2.12%'], ['PFE', 34.34, '3.99%'], ['CVX', 115.18, '3.92%'], ['MCD', 214.66, '2.05%'], ['JPM', 106.02, '2.94%'], ['JNJ', 127.73,
'2.78%'], ['V', 175.23, '0.56%'], ['XOM', 67.49, '4.79%'], ['GS', 196.2, '1.61%'], ['MMM', 155.85, '3.48%'], ['MSFT', 133.39, '1.34%'], ['DOW', 40.71, '1.66%'], ['WBA', 49.32, '3.45%'], ['DIS', 131.67, '1.29%'], ['CAT', 114.06, '3.06%'], ['CSCO', 46.61, '2.82%'], ['NKE', 80.44, '1.03%'], ['IBM', 129.57, '4.71%'], ['UTX', 123.42, '2.27%'], ['AXP', 117.76, '1.28%'], ['INTC', 44.96, '2.63%'], ['AAPL', 202.64, '1.39%']])
    [['XOM', 67.49, '4.79%'], ['VZ', 55.92, '4.24%'], ['PFE', 34.34, '3.99%'], ['WBA', 49.32, '3.45%'], ['KO', 53.74, '2.90%']]
    >>>dl5([['XOM', 67.49, '4.79%'], ['VZ', 55.92, '4.24%'], ['PFE', 34.34, '3.99%'], ['WBA', 49.32, '3.45%'], ['KO', 53.74, '2.90%'], ['CSCO', 46.61, '2.82%'], ['INTC', 44.96, '2.63%'], ['MRK', 84.94, '2.38%'], ['DOW', 40.71, '1.66%'], ['NKE', 80.44, '1.03%']])
    [['XOM', 67.49, '4.79%'], ['VZ', 55.92, '4.24%'], ['PFE', 34.34, '3.99%'], ['WBA', 49.32, '3.45%'], ['KO', 53.74, '2.90%']]
    '''

    #Sorts the list according to the current stock price from lowest to highest
    result = sorted(raw, key = itemgetter(1))

    #Leaves the top 10 lowest priced stocks
    for i in range(10, len(raw)):
        result.pop()

    #Sorts the list according to dividend from highest to lowest
    result = sorted(result, key = itemgetter(2), reverse = True)

    #Leaves the top 5 highest dividend stocks
    for i in range(4, 9):
        result.pop()

    return result