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


def main():
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    driver.get('https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n&sat')

    # https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n&sat=01

    # hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']

    hours = ['00', '01']

    dataList = []

    sleep(5)

    for hour in hours:

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'table-aktualni-podaci'))
        )

        hourElement = driver.find_element(By.XPATH, f'//ul[@class="hours-browser-v2__hours"]/li/*[contains(text(), "{hour}")]')
        hourElement.click()

        sleep(5)

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'table-aktualni-podaci'))
        )

        columnTitlesElements = driver.find_elements(By.XPATH, '//div[@class="fd-c-table--responsive fd-u-display--none fd-u-md-display--block"]/table/thead/tr/th')

        columnTitles = [col.text.replace('\n', ' ') for col in columnTitlesElements]
        numberOfColumns = len(columnTitles)

        dataElements = driver.find_elements(By.XPATH, '//div[@class="fd-c-table--responsive fd-u-display--none fd-u-md-display--block"]/table/tbody/tr/td')

        data = [re.sub(' A$|\*$', '', dat.text) for dat in dataElements]

        dataProcessed = []
        if len(data) % numberOfColumns == 0:
            for i in range(len(data) // numberOfColumns):
                dataProcessed.append(data[i*numberOfColumns:(i+1)*numberOfColumns])

        columnTitles.append('Datum i vrijeme')
        dateElement = driver.find_element(By.XPATH, '//div[@class="glavni__content"]/*/h4').text
        date = dateElement.replace('Vrijeme u Hrvatskoj ', '').replace(' u', '').replace(' h', 'h')

        for i in range(len(dataProcessed)):
            dataProcessed[i].append(date)

        df = pd.DataFrame(dataProcessed, columns=columnTitles)
        print(f'Vrijeme u {hour} sati:')
        print(df.head(10))
        # dataFrameList.append(df)

        # df.to_csv('dhmz_podaci.csv')

    # with open('podaci.pkl', 'w') as f:
    #     pickle.dump(dataFrameList, f)

    driver.quit()


def getData():
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    driver.get('https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n&sat')

    # https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n&sat=01

    hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']

    # hours = ['00']

    dataList = []

    sleep(1)

    for hour in hours:

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'table-aktualni-podaci'))
        )

        hourElement = driver.find_element(By.XPATH, f'//ul[@class="hours-browser-v2__hours"]/li/*[contains(text(), "{hour}")]')
        hourElement.click()

        sleep(1)

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'table-aktualni-podaci'))
        )


        dataElements = driver.find_elements(By.XPATH, '//div[@class="fd-c-table--responsive fd-u-display--none fd-u-md-display--block"]/table/tbody/tr/td')

        data = [re.sub(' A$|\*$', '', dat.text) for dat in dataElements]

        dataProcessed = []
        if len(data) % 8 == 0:
            for i in range(len(data) // 8):
                dataProcessed.append(data[i*8:(i+1)*8])

        dateElement = driver.find_element(By.XPATH, '//div[@class="glavni__content"]/*/h4').text
        date = dateElement.replace('Vrijeme u Hrvatskoj ', '').replace(' u', '').replace(' h', 'h')

        for entry in dataProcessed:
            e = {
                'postaja': entry[0],
                'vjetar_smjer': entry[1],
                'vjetar_brzina': float(entry[2]) if entry[2] != '-' else 0,
                'temperatura_zraka': float(entry[3]) if entry[3] != '-' else 0,
                'relativna_vlaznost': entry[4],
                'tlak_zraka': float(entry[5]) if entry[5] != '-' else 0,
                'tendencija_tlaka': entry[6],
                'stanje_vremena': entry[7],
                'datum_i_vrijeme': date
            }

            dataList.append(e)
    
    with open('data.txt', 'w', encoding='utf-8') as f:
        json.dump(dataList, f)

    driver.quit()


if __name__ == '__main__':
    getData()