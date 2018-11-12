import pandas as pd
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


def getHistoricalPrice(start, end):

    #Setting dates to site's format
    start = start.strftime('%d/%m/%Y')
    end = end.strftime('%d/%m/%Y')

    #All listed stocks on the Lisbon Stock Exchange
    stockISIN = \
        ['PTALT0AE0002', 'PTBCP0AM0015', 'PTBPI0AM0004', 'PTSLB0AM0010', 'PTCFN0AE0003', 'PTCOM0AE0007', 'PTCOR0AE0006',
        'PTCTT0AM0001', 'PTEDP0AM0009', 'ES0127797019', 'PTESO0AM0000', 'NL0006294274', 'PTFCP0AM0008', 'PTGAL0AM0009',
        'PTPAD0AM0007', 'PTIBS0AM0008', 'PTGPA0AP0007', 'PTIPR0AM0000', 'PTINA0AP0008', 'PTINA2VP0019', 'PTIAN0AM0001',
        'PTJMT0AE0001', 'PTLIG0AE0002', 'PTEPT0AM0005', 'PTMFR0AM0003', 'PTGMC0AM0003', 'PTMEN0AE0005', 'PTNEX0AM0002',
        'PTZON0AM0006', 'PTNBA0AM0006', 'PTORE0AM0002', 'PTPRS0AM0009', 'PTPTC0AM0009', 'PTFRV0AE0004', 'PTRED0AP0010',
        'PTREL0AM0008', 'PTSAG0AE0004', 'PTSEM0AM0004', 'PTSON0AM0001', 'PTSNP0AE0008', 'PTS3P0AM0025', 'PTSNC0AM0006',
        'PTSCP0AM0001', 'PTTD10AM0000', 'PTPTI0AM0006', 'PTSCT0AP0018', 'PTVAA0AM0019']

    stockName = \
    ['ALTR', 'BCP', 'BPI', 'SLBEN', 'CFN', 'COMAE', 'COR', 'CTT', 'EDP', 'EDPR', 'ESON','ENXP', 'FCP', 'GALP', 'GLINT',
     'IBS', 'GPA', 'IPR', 'INA', 'INAP', 'ALISA', 'JMT', 'LIG', 'LUZ', 'MAR', 'MCP', 'EGL', 'ALNOR', 'NOS', 'NBA', 'ORE',
     'ALPTR', 'PHR', 'RAM', 'RED', 'RENE', 'SVA', 'SEM', 'SON', 'SONC', 'SONI', 'SNC', 'SCP', 'TDSA', 'NVG', 'SCT', 'VAF']

    [getStockHistory(eachStock, start, end) for eachStock in stockISIN]

    return 'Done'


def getStockHistory(eachStock, start, end):

    try:
        # Defining path to driver
        driverPath = os.path.join('/Users/Robson/Downloads', 'chromedriver')

        url = 'https://www.bolsadelisboa.com.pt/pt-pt/products/equities/'+ eachStock +'-XLIS/quotes'
        # driver = webdriver.Firefox()
        driver = webdriver.Chrome(executable_path=driverPath)
        driver.implicitly_wait(10)
        driver.get(url)

        #Clicking on  button
        driver.find_element_by_id('pcContainer_da').send_keys(Keys.ENTER) # View Data
        time.sleep(5)
        driver.find_element_by_id('tablesNavigation_hi').send_keys(Keys.ENTER) # Historical

        time.sleep(5)

        # selecting the start datepicker by id and filling with start date inputted by the user
        startPicker = driver.find_element_by_id('historicalDatePicker1')
        startPicker.click()
        driver.find_element_by_class_name('second-row').click()
        startPicker.clear()
        startPicker.send_keys(start)
        #tabbing because it what worked
        startPicker.send_keys(Keys.TAB)

        time.sleep(3)

        # selecting the start datepicker by id and filling with start date inputted by the user
        endPicker = driver.find_element_by_id('historicalDatePicker2')
        endPicker.click()
        endPicker.send_keys(Keys.ESCAPE)
        endPicker.clear()
        endPicker.send_keys(end)

        driver.find_element_by_id('refreshHistoricalPC').send_keys(Keys.ENTER) #Refresh
        driver.find_element_by_id('downloadPCTable').send_keys(Keys.ENTER) #Download

        time.sleep(3)

    # inject the JavaScript...

        try:
            driver.execute_async_script("document.querySelectorAll('button.ui-state-default.ui-corner-all')[3].click()")

        except:

            driver.quit()
            pass

    except:
        pass

    return 'Done'

if '__main__' == __name__:

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime(2018, 11, 12)

    getHistoricalPrice(start, end)