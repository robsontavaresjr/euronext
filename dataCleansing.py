import pandas as pd
import datetime as dt
import os

def getCSV(path):

    counter = 0
    stockName, stockISIN = getDeParaStocks()
    calendar = setBusinessDays()

    for files in os.listdir(path):
        try:
            print(files)

            if counter == 0:

                df = pd.read_csv(os.path.join(path, files), skiprows=3) #read the table data
                df = df[['Data', 'ISIN', 'Abrir', u'Máximo', u'Mínimo', 'Close', 'Number of Shares']] #select the columns
                df.ISIN = df.ISIN.apply(lambda x: stockName[stockISIN.index(x)]) # transform ISIN in ticker
                df.columns = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume'] # rename the columns
                df.Date = df.Date.apply(lambda x: dt.datetime.strptime(x, '%d/%m/%Y')) # transform date in dt.datetime
                df = calendar.merge(df, how='left', on='Date') # merge with business day to have all data points
                df.fillna(method='ffill', inplace=True) #filling NaN with last value of the dataframe
                df.Ticker.fillna(method='bfill', inplace=True)
                df.fillna(0, inplace=True)

            else:

                df2 = pd.read_csv(os.path.join(path, files), skiprows=3) #read the table data
                df2 = df2[['Data', 'ISIN', 'Abrir', u'Máximo', u'Mínimo', 'Close', 'Number of Shares']] #select the columns
                df2.ISIN = df2.ISIN.apply(lambda x: stockName[stockISIN.index(x)]) # transform ISIN in ticker
                df2.columns = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume'] # rename the columns
                df2.Date = df2.Date.apply(lambda x: dt.datetime.strptime(x, '%d/%m/%Y')) # transform date in dt.datetime
                df2 = calendar.merge(df2, how='left', on='Date') # merge with business day to have all data points
                df2.fillna(method='ffill', inplace=True) #filling NaN with last value of the dataframe
                df2.Ticker.fillna(method='bfill', inplace=True)
                df2.fillna(0, inplace=True)


                df = df.append(df2, ignore_index=True) # append to a larger dataframe containing all tickers

            counter += 1

        except:
            pass

    df.to_pickle("./stock.pkl")

    return df

def setBusinessDays():

    holidays = \
        ['2010-01-01', '2010-04-02', '2010-04-05', '2011-04-22', '2011-04-25', '2011-12-26', '2012-04-06',
         '2012-04-09', '2012-05-01', '2012-12-25', '2012-12-26', '2013-01-01', '2013-03-29', '2013-04-01',
         '2013-05-01', '2013-12-25', '2013-12-26', '2014-01-01', '2014-04-18', '2014-04-21', '2014-05-01',
         '2014-12-25', '2014-12-26', '2015-01-01', '2015-04-03', '2015-04-06', '2015-05-01', '2015-12-25',
         '2016-01-01', '2016-03-25', '2016-03-28', '2016-12-26', '2017-04-14', '2017-04-17', '2017-05-01',
         '2017-12-25', '2017-12-26', '2018-01-01', '2018-03-20', '2018-04-02', '2018-05-01', '2018-12-25',
         '2018-12-26']


    start = dt.datetime(2010, 1, 1)
    end = dt.datetime(2018, 11, 9)

    numDays = end - start
    numDays = numDays.days

    calendar = []

    for days in list(range(numDays)):

        checkDate = start + dt.timedelta(days=days)

        if  (checkDate.strftime('%Y-%m-%d') in holidays) or (checkDate.weekday() in [5,6]):
            pass
        else:
            calendar.append(checkDate)

    calendar = pd.DataFrame(calendar)
    calendar.columns = ['Date']

    return calendar

def getDeParaStocks():
    stockISIN = \
        ['PTALT0AE0002', 'PTBCP0AM0015', 'PTBPI0AM0004', 'PTSLB0AM0010', 'PTCFN0AE0003', 'PTCOM0AE0007',
         'PTCOR0AE0006',
         'PTCTT0AM0001', 'PTEDP0AM0009', 'ES0127797019', 'PTESO0AM0000', 'NL0006294274', 'PTFCP0AM0008',
         'PTGAL0AM0009',
         'PTPAD0AM0007', 'PTIBS0AM0008', 'PTGPA0AP0007', 'PTIPR0AM0000', 'PTINA0AP0008', 'PTINA2VP0019',
         'PTIAN0AM0001',
         'PTJMT0AE0001', 'PTLIG0AE0002', 'PTEPT0AM0005', 'PTMFR0AM0003', 'PTGMC0AM0003', 'PTMEN0AE0005',
         'PTNEX0AM0002',
         'PTZON0AM0006', 'PTNBA0AM0006', 'PTORE0AM0002', 'PTPRS0AM0009', 'PTPTC0AM0009', 'PTFRV0AE0004',
         'PTRED0AP0010',
         'PTREL0AM0008', 'PTSAG0AE0004', 'PTSEM0AM0004', 'PTSON0AM0001', 'PTSNP0AE0008', 'PTS3P0AM0025',
         'PTSNC0AM0006',
         'PTSCP0AM0001', 'PTTD10AM0000', 'PTPTI0AM0006', 'PTSCT0AP0018', 'PTVAA0AM0019']

    stockName = \
        ['ALTR', 'BCP', 'BPI', 'SLBEN', 'CFN', 'COMAE', 'COR', 'CTT', 'EDP', 'EDPR', 'ESON', 'ENXP', 'FCP', 'GALP',
         'GLINT',
         'IBS', 'GPA', 'IPR', 'INA', 'INAP', 'ALISA', 'JMT', 'LIG', 'LUZ', 'MAR', 'MCP', 'EGL', 'ALNOR', 'NOS',
         'NBA', 'ORE',
         'ALPTR', 'PHR', 'RAM', 'RED', 'RENE', 'SVA', 'SEM', 'SON', 'SONC', 'SONI', 'SNC', 'SCP', 'TDSA', 'NVG',
         'SCT', 'VAF']

    return stockName, stockISIN



if __name__ == '__main__':

    path = '/Users/Robson/Downloads/stock'
    getCSV(path)
    # df = pd.read_pickle("./stock.pkl")
    # print(df)
    # calendar = setBusinessDays()
    # os.remove("./stock.pkl")
