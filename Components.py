from bs4 import BeautifulSoup
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