from bs4 import BeautifulSoup
from operator import itemgetter

import re
import urllib.request


def dl5MW(url, stocks):
    ''' (url, list) -> list

    Return the DOW Low 5 using Market Watch.

    >>>dl5MW("https://www.marketwatch.com/investing/stock/", ['MMM', 'AXP', 'BA', 'CAT', 'CVX', 'KO', 'DIS', 'DOW', 'GS', 'HD', 'IBM', 'JNJ', 'JPM', 'MCD', 'MRK', 'NKE', 'PG', 'CRM', 'TRV', 'UNH', 'VZ', 'V', 'WMT'])
    [['IBM', '128.62', '5.09%'], ['MMM', '148.74', '4.02%'], ['CVX', '161.00', '3.51%'], ['JPM', '140.10', '2.86%'], ['JNJ', '175.00', '2.43%']]
    '''

    raw = []

    # Merge each stock in a list with its current price and dividend
    for item in stocks:
        html = urllib.request.urlopen(url + item)
        soup = BeautifulSoup(html, "lxml")

        raw.append([item,
                    soup.find("bg-quote", attrs={"class": "value"}).text,
                    (soup.find("small", text="Yield")).find_next_sibling("span").text])

    # Sort the list according to the current stock price from lowest to highest
    result = sorted(raw, key=itemgetter(1))

    # Leave the top 10 lowest priced stocks
    for i in range(10, len(raw)):
        result.pop()

    # Sort the list according to dividend from highest to lowest
    result = sorted(result, key=itemgetter(2), reverse=True)

    # Leave the top 5 highest dividend stocks
    for i in range(4, 9):
        result.pop()

    print(
        "The below is the DOW Low 5 in the format of [STOCK, CURRENT PRICE, DIVIDEND]:", *result, sep="\n")

    return result


def stocksWiki(url):
    ''' (string) -> list

    Take the Wikipedia URL to components of an index and grab the individual stock names.

    >>>stocks("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    ['MMM', 'AXP', 'BA', 'CAT', 'CVX', 'KO', 'DIS', 'DOW', 'GS', 'HD', 'IBM', 'JNJ', 'JPM', 'MCD', 'MRK', 'NKE', 'PG', 'CRM', 'TRV', 'UNH', 'VZ', 'V', 'WMT']
    '''

    tickers = []
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "lxml")

    # Find the table that contains the index components
    table = soup.find("table", id="constituents")

    # Get links that contain the ticker
    links = table.find_all("a", href=re.compile(r"quote"))

    # Place ticker into a list
    for a in links:
        tickers.append(a.text)

    print("The components are:\n", tickers)

    return tickers


@DeprecationWarning
def currentPriceYahoo(url, stocks):
    ''' (string, list) -> list

    Return a list of current prices for each stock respectively.

    >>>currentPriceYahoo("https://ca.finance.yahoo.com/quote/", ["MSFT"])
    ['137.78']
    >>>currentPriceYahoo("https://ca.finance.yahoo.com/quote/", ["WMT", "INTL", "FEYE"])
    ['111.91', '38.74', '13.57']
    '''

    result = []

    # Take each stock and get its current price
    for item in stocks:
        html = urllib.request.urlopen(url + item)
        soup = BeautifulSoup(html, "lxml")

        # NOTE: Another way is to grab the location of "At close" text and find the stock price from there
        result.append(soup.select_one(
            'span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\)').text)

    return result


@DeprecationWarning
def dividendYahoo(url, path, stocks):
    ''' (string, string, list) -> list

    Return the trailing dividend yield of each stock respectively.

    >>>dividendYahoo("https://ca.finance.yahoo.com/quote/", "/key-statistics", ["MSFT"])
    ['1.33%']
    >>>dividendYahoo("https://ca.finance.yahoo.com/quote/", "/key-statistics", ["WMT", "INTL", "FEYE"])
    ['1.87%', 'N/A', 'N/A']
    '''

    result = []

    # Take each stock and gets their trailing annual dividend yield
    for item in stocks:
        html = urllib.request.urlopen(url + item + path)
        soup = BeautifulSoup(html, "lxml")

        result.append(soup.find(
            text="Trailing Annual Dividend Yield").parent.parent.nextSibling.text)

    return result


@DeprecationWarning
def dl5Yahoo(raw):
    ''' (list) -> (list)

    Return the DOW Low 5 stocks.

    >>>dl5Yahoo([['BA', 356.01, '2.12%'], ['WMT', 110.83, '1.88%'], ['UNH', 230.66, '1.62%'], ['KO', 53.74, '2.90%'], ['VZ', 55.92, '4.24%'], ['HD', 217.47, '2.31%'], ['PG', 117.32, '2.43%'], ['MRK', 84.94, '2.38%'], ['TRV', 144.73, '2.12%'], ['PFE', 34.34, '3.99%'], ['CVX', 115.18, '3.92%'], ['MCD', 214.66, '2.05%'], ['JPM', 106.02, '2.94%'], ['JNJ', 127.73,
'2.78%'], ['V', 175.23, '0.56%'], ['XOM', 67.49, '4.79%'], ['GS', 196.2, '1.61%'], ['MMM', 155.85, '3.48%'], ['MSFT', 133.39, '1.34%'], ['DOW', 40.71, '1.66%'], ['WBA', 49.32, '3.45%'], ['DIS', 131.67, '1.29%'], ['CAT', 114.06, '3.06%'], ['CSCO', 46.61, '2.82%'], ['NKE', 80.44, '1.03%'], ['IBM', 129.57, '4.71%'], ['UTX', 123.42, '2.27%'], ['AXP', 117.76, '1.28%'], ['INTC', 44.96, '2.63%'], ['AAPL', 202.64, '1.39%']])
    [['XOM', 67.49, '4.79%'], ['VZ', 55.92, '4.24%'], ['PFE', 34.34, '3.99%'], ['WBA', 49.32, '3.45%'], ['KO', 53.74, '2.90%']]
    >>>dl5Yahoo([['XOM', 67.49, '4.79%'], ['VZ', 55.92, '4.24%'], ['PFE', 34.34, '3.99%'], ['WBA', 49.32, '3.45%'], ['KO', 53.74, '2.90%'], ['CSCO', 46.61, '2.82%'], ['INTC', 44.96, '2.63%'], ['MRK', 84.94, '2.38%'], ['DOW', 40.71, '1.66%'], ['NKE', 80.44, '1.03%']])
    [['XOM', 67.49, '4.79%'], ['VZ', 55.92, '4.24%'], ['PFE', 34.34, '3.99%'], ['WBA', 49.32, '3.45%'], ['KO', 53.74, '2.90%']]
    '''

    # Sort the list according to the current stock price from lowest to highest
    result = sorted(raw, key=itemgetter(1))

    # Leave the top 10 lowest priced stocks
    for i in range(10, len(raw)):
        result.pop()

    # Sort the list according to dividend from highest to lowest
    result = sorted(result, key=itemgetter(2), reverse=True)

    # Leave the top 5 highest dividend stocks
    for i in range(4, 9):
        result.pop()

    return result


@DeprecationWarning
def mergeYahoo(listOne, listTwo, listThree):
    ''' (list, list, list) -> list

    Merges three lists.

    >>>mergeYahoo(['PG'], ['118.71'], ['2.43%'])
    [['PG', '118.71', '2.43%']]
    >>>mergeYahoo(['UNH', 'VZ', 'CVX'], ['231.22' '56.27' '116.56'], ['1.62%', '4.24%', '3.92%'])
    [['UNH', '231.22', '1.62%'], ['VZ', '56.27', '4.24%'], ['CVX', '116.56', '3.92%']]
    '''

    length = len(listOne)
    result = []

    for i in range(length):
        result.insert(i, [listOne[i], float(listTwo[i]), listThree[i]])

    return result


@DeprecationWarning
def stocksYahoo(url):
    ''' (string) -> list

    Take the Yahoo URL to components of an index and grab the individual stock names.

    >>>stocksYahoo("https://ca.finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI")
    ['DIS', 'WBA', 'IBM', 'MMM', 'PG', 'XOM', 'VZ', 'AAPL', 'CVX', 'MRK', 'JNJ', 'AXP', 'UTX', 'CAT', 'INTC', 'HD', 'V', 'WMT', 'KO', 'PFE', 'NKE', 'TRV', 'MCD', 'GS', 'MSFT', 'JPM', 'CSCO', 'DOW', 'UNH', 'BA']

    >>>stocksYahoo("https://ca.finance.yahoo.com/quote/%5EIXIC/components?p=%5EIXIC")
    ['FNKO', 'SLAB', 'FEYE', 'FARO', 'TSLA', 'CVCY', 'FNLC', 'IBKC', 'SPHS', 'NVCR', 'FRTA', 'EXAS', 'CMRX', 'ATEC', 'IFRX', 'AGLE', 'CVCO', 'OPTT', 'NVCN', 'NMRK', 'POPE', 'TBIO', 'SCON', 'KLXE', 'FRSX', 'FNJN', 'AKTX', 'FARM', 'TWST', 'SCOR']
    '''

    html = urllib.request.urlopen(url)
    titles = []
    soup = BeautifulSoup(html, "lxml")

    # Find the <a> tags in the table that comprises the components of the index and grab the title attribute
    for a in soup.tbody.find_all('a'):
        titles.append(a.get('title'))

    return titles
