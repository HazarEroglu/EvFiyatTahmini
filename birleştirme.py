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
def listToString(s):  
    
    str1 = " " 
  
    return (str1.join(s))

service = Service(executable_path='C:\\Users\\Hazar\\Desktop\\evfiyattahminproje\\geckodriver.exe')
firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(service=service, options=firefox_options)
firefox_options.add_argument("--headless")

URL = 'https://www.emlakjet.com/satilik-konut/mugla-marmaris/'
driver.get(URL)
driver.maximize_window()

counter = 1
while counter<7:
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@data-index='{counter}']"))
        )
        element.click()

        elements = driver.find_elements(By.CSS_SELECTOR,"._3tH_Nw")
        mahalle = driver.find_elements(By.CSS_SELECTOR,"#harita > div > div._2VNNor > div > div._3VQ1JB > p")    
        fiyatlar = driver.find_elements(By.CSS_SELECTOR,"._2TxNQv")

        mahalleList = []
        detaylar = []
        fiyat = []
        for i in fiyatlar:
            #print(i.text)
            fiyat.append(i.text)                        # özellikleri stringe çevirerek listeye atýyoruz. 
        
    
        for i in elements:
            #print(i.text)
            detaylar.append(i.text)                     # özellikleri stringe çevirerek listeye atýyoruz.

        for i in mahalle:
            mahalleList.append(i.text) 
      
        det_str = listToString(detaylar)
        ayri= det_str.split("\n")
        df = pd.DataFrame(ayri)
        det_str2 = listToString(detaylar)
        ayri2 = det_str2.split("\n")
        df2 = pd.DataFrame(ayri2)
        df_yeni = df.iloc[6:12] 
        df_yeni2 = df2.iloc[18:24]                        #integer location
        df_yeni = df_yeni.reset_index()
        df_yeni2 = df_yeni2.reset_index()
        df_yeni.drop("index", axis = 1, inplace = True) #parantez içindeki sayýlardan kurtulmak için
        df_yeni2.drop("index", axis = 1, inplace = True)
        df_liste = df_yeni.values.tolist() 
        df_liste2 = df_yeni2.values.tolist()           

        mh_str = listToString(mahalleList)
        mh_parcalar = mh_str.split("-")
        mh_kismi = mh_parcalar[-1].strip()
        mhsiz_kisim = mh_kismi.split(" ")
        mhsiz_kisim_ayir = mhsiz_kisim[0].strip()

        icerikler =[]
        icerikler.append(mhsiz_kisim_ayir)
        i = 1
        while i <= 4:
            #print(df_liste[i])
            icerikler.append(df_liste[i])
            i = i+2
        i = 1
        while i <= 5:
            #print(df_liste[i])
            icerikler.append(df_liste2[i])
            i = i+2
        fiyat_sade = fiyat[1].strip()
        fiyat_sade = fiyat_sade.replace("TL","")     #fiyatýn TL kýsmýný sildik
        icerikler.append([fiyat_sade])
    
        driver.execute_script("window.scrollBy(0, -500)")
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/div[2]"))
        )
        element.click()  
        time.sleep(3)  
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/ymaps/ymaps/ymaps/ymaps[3]/ymaps[2]/ymaps/ymaps[1]/ymaps/ymaps[2]/ymaps"))
        )                  # /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/ymaps/ymaps/ymaps/ymaps[3]/ymaps[2]/ymaps/ymaps[1]/ymaps/ymaps[2]
        element.click()  
        time.sleep(3)  
        """
        all_handles = driver.window_handles
        driver.switch_to.window(all_handles[-1])
        time.sleep(3) 
        driver.close()
        driver.switch_to.window(all_handles[0])
        time.sleep(3)  
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/ymaps/ymaps/ymaps/ymaps[3]/ymaps[2]/ymaps/ymaps[1]/ymaps/ymaps[2]/ymaps"))
        )
        element.click()  
        time.sleep(6) 
        """
        all_handles = driver.window_handles
        driver.switch_to.window(all_handles[-1])

        og_type = driver.find_element(By.CSS_SELECTOR,'meta[property="og:url"]').get_attribute("content")
        #print(og_type)
        parsed_url = urlparse(og_type)
        query_parameters = parse_qs(parsed_url.query)
        ll_param = query_parameters.get('rtext', [''])[0]
        ll_param = ll_param.replace('~', '')
        latitude, longitude = map(float, ll_param.split(','))
        icerikler.append([ll_param])
        df_icerikler = pd.DataFrame(icerikler).T
        df_icerikler.to_csv(r"ilk.csv",encoding="utf-8",index=True, mode="a")
        

        driver.close()
        driver.switch_to.window(all_handles[0])
        driver.back()
        counter += 1
        if (counter == 7):
            counter = 8
        if (counter == 21):
             counter = 22
        if (counter == 14):
             counter = 15   
        
            
    except Exception as e:
        driver.execute_script("window.scrollBy(0,100)","")
    
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    


