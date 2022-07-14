import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#THIS IS A PRACTICE BRANCH
# read csv_file into a pandas dataframe object
with open('Python Quiz Input - Sheet1.csv', mode='r',newline='') as csv_file:
    address_df = pd.read_csv(csv_file)



# site URL for scraping
USPS_URL = "https://tools.usps.com/zip-code-lookup.htm?byaddress"

# enable browser console reading capabilities
dc = DesiredCapabilities.CHROME
dc['goog:loggingPrefs'] = { 'browser':'ALL' }

# set up driver
service= Service("C:/Users...Webdriver/chromedriver")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, desired_capabilities=dc, options=op)


# function to run driver with csv data-  returns True/False if address is valid or not.

def run_driver(row):
    driver.get(USPS_URL)
    driver.implicitly_wait(1)
    company_input = driver.find_element(By.ID, 'tCompany')
    street_input = driver.find_element(By.ID, 'tAddress')
    city_input = driver.find_element(By.ID, 'tCity')
    state_select = driver.find_element(By.ID, 'tState')
    StateSelect = Select(state_select)
    zip_input = driver.find_element(By.ID, 'tZip-byaddress')
    find_button = driver.find_element(By.ID, 'zip-by-address')
    company_input.send_keys(row['Company'])
    street_input.send_keys(row['Street'])
    city_input.send_keys(row['City'])
    StateSelect.select_by_value(row['St'])
    zip_input.send_keys(row['ZIPCode'])
    find_button.click()
    time.sleep(1) #to give time for error to be printed in console
    for entry in driver.get_log('browser'):
        if len(entry) > 0:
            return False
        else:
            return True

# list of new column
address_validity=[]


# run script with csv data- creates new column of valid/invalid addresses
for index, row in address_df.iterrows():
    if run_driver(row=row) == False:
        address_validity.append('Invalid')
    else:
        address_validity.append('Valid Address')
driver.quit()

# add column of validity to addresses
address_df['Validity'] = address_validity

#write new csv_file with new column
address_df.to_csv('finished.csv')





