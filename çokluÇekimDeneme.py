
# -- coding: utf-8 --
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urlparse, parse_qs

service = Service(executable_path='C:\\Users\\Hazar\\Desktop\\evfiyattahminproje\\geckodriver.exe')
firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(service=service, options=firefox_options)
firefox_options.add_argument("--headless")

URL = 'https://www.emlakjet.com/satilik-konut/mugla-marmaris/'
driver.get(URL)
driver.maximize_window()

counter = 1
while counter < 20:
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@data-index='{counter}']"))
        )
        element.click()
        time.sleep(3)  # Yeterli zaman ekleyin
        driver.back()  # Geri dön
        time.sleep(3)
        counter += 1
        if (counter == 7):
            counter = 8
        if (counter == 21):
            counter = 22
        if (counter == 14):
            counter = 15    
        print(counter)
        print("\n")
    except Exception as e:
        driver.execute_script("window.scrollBy(0,100)","")

