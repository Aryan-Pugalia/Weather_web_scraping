# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import os

def Year(year):

    def month(i):
        return 'https://www.wunderground.com/history/monthly/in/new-delhi/VIDP/date/'+str(year)+'-'+str(i+1)
    # Create empty DataFrame for the Weather Data
    weather_df = pd.DataFrame({'month0':[], 'Max1':[], 'Avg1':[], 'Min1':[], 'Max2':[], 'Avg2':[], 'Min2':[], 'Max3':[],
        'Avg3':[], 'Min3':[], 'Max4':[], 'Avg4':[], 'Min4':[], 'Max5':[], 'Avg5':[], 'Min5':[],
        'Total6':[]})


    for i in range(12):
        URL = month(i)
        # Adjust the path to the location where you've placed the chromedriver
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.headless = True

        # Setup the Firefox Service
        service = Service('C:\drivers\geckodriver-v0.33.0-win64\geckodriver.exe')

        # Create a new instance of the Firefox driver with the specified options and service
        driver = webdriver.Firefox(service=service, options=firefox_options)

        driver.get(URL)
        # Wait for the page to load (or a specific element, like the table, if necessary)
        try:
            element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "table")))
        except:
            driver.quit()
            continue
        # Step 2: Parse the contents with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        df = pd.DataFrame()
        driver.quit()

        table = soup.find_all('table')[1]


        tbs = table.find_all('table')

        for tb in range(len(tbs)):
            tbs1 = [i.text.strip() for i in tbs[tb].find_all('tr')]
            
            tbs2 = [i.split('  ') for i in tbs1]
            if tbs2[0] not in [['Total'],['Max','Avg','Min']]:
                temp = tbs1[0]
                tbs2[0]=['month']
                tbs2[1:]=[[temp+'-'+i[0]] for i in tbs2[1:]]
            tbs_head = [i + str(tb)  for i in tbs2[0]]
            
            df[tbs_head]=tbs2[1:]

        
        weather_df = pd.concat([weather_df,df],axis=0,ignore_index=True)
    # Make a folder in the current working dir and change cwd to that   
    os.mkdir('Weather_Data')
    os.chdir('Weather_Data')
    
    path = "Year_"+str(year)+".csv"
    # Change columns names
    weather_df.columns = ['Month', 'Max_Temperature', 'Avg_Temperature', 'Min_Temperature', 'Max_Dew_Point', 'Avg_Dew_Point', 'Min_Dew_Point', 'Max_Humidity',
        'Avg_Humidity', 'Min_Humidity', 'Max_Wind_Speed', 'Avg_Wind_Speed', 'Min_Wind_Speed', 'Max_Pressure', 'Avg_Pressure', 'Min_Pressure',
        'Total_Precipitation']
    # Transfer the DataFrame to cwd
    weather_df.to_csv(path)

if __name__=='__main__':
    for i in range(2000,2001):
        Year(i)

