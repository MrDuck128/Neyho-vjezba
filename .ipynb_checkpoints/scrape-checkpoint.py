from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get('https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n')

# https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n&sat=01

WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.ID, 'table-aktualni-podaci'))
)

columnTitles = driver.find_element(By.XPATH, '//table[@id="table-aktualni-podaci"]/thead/tr/th')




sleep(8)

driver.quit()

