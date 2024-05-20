from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re
import pandas as pd
import pickle
import json

def getData():
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    driver.get('https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n&sat')

    # https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n&sat=01

    # hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
    hours = ['12']

    dataList = []

    for hour in hours:

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'table-aktualni-podaci'))
        )

        hourElement = driver.find_element(By.XPATH, f'//ul[@class="hours-browser-v2__hours"]/li/*[contains(text(), "{hour}")]')
        hourElement.click()

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'table-aktualni-podaci'))
        )

        dataElements = driver.find_elements(By.XPATH, '//div[@class="fd-c-table--responsive fd-u-display--none fd-u-md-display--block"]/table/tbody/tr/td')

        data = [re.sub(' A$|\*$', '', dat.text) for dat in dataElements]

        dataProcessed = []
        if len(data) % 8 == 0:
            for i in range(len(data) // 8):
                dataProcessed.append(data[i*8:(i+1)*8])

        dateElement = driver.find_element(By.XPATH, '//div[@class="glavni__content"]/*/h4').text.split(' ')
        date, time = dateElement[3], dateElement[5]

        for entry in dataProcessed:
            e = {
                'postaja': entry[0],
                'vjetar_smjer': entry[1],
                'vjetar_brzina': float(entry[2]) if entry[2] != '-' else '-',
                'temperatura_zraka': float(entry[3]) if entry[3] != '-' else '-',
                'relativna_vlaznost': int(entry[4]) if entry[4] != '-' else '-',
                'tlak_zraka': float(entry[5]) if entry[5] != '-' else '-',
                'tendencija_tlaka': entry[6],
                'stanje_vremena': entry[7],
                'datum': date,
                'vrijeme': time
            }

            dataList.append(e)

        if dfPrint:
            columnTitlesElements = driver.find_elements(By.XPATH, '//div[@class="fd-c-table--responsive fd-u-display--none fd-u-md-display--block"]/table/thead/tr/th')
            columnTitles = [col.text.replace('\n', ' ') for col in columnTitlesElements]
            numberOfColumns = len(columnTitles)

            columnTitles.append('Datum i vrijeme')

            for i in range(len(dataProcessed)):
                dataProcessed[i].append(f'{date} u {time}h')

            df = pd.DataFrame(dataProcessed, columns=columnTitles)
            print(f'Vrijeme u {hour} sati:')
            print(df.head(10))
            # df.to_csv('dhmz_podaci.csv')
    
    with open('data.txt', 'w', encoding='utf-8') as f:
        json.dump(dataList, f)

    driver.quit()


if __name__ == '__main__':
    dfPrint = 1
    getData()