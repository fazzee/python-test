from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import csv
import re


driver = webdriver.Chrome()
driver.get("https://itdashboard.gov/")

try:
    main = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(.,'DIVE IN')]"))
    )
    main.click()

except:
     driver.quit()
     
agency_list=driver.find_element_by_xpath("//*[@id='agency-tiles-widget']/div").text


#dynamic agencies
list=[]
time.sleep(10)
numberOfRows = len(driver.find_elements_by_xpath('//*[@id="agency-tiles-widget"]/div/div'))
for iRow in range(numberOfRows):
    # print(iRow)
 
        numberOfColumns = driver.find_elements_by_xpath('//*[@id="agency-tiles-widget"]/div/div['+str(iRow+1)+']/div')
        for i in range(len(numberOfColumns)):
            class WebElement(object):
             content=numberOfColumns[i]
             agency = WebDriverWait(content, 10).until(
                 EC.presence_of_element_located((By.XPATH, './div/div/div/div[1]/a/span[1]'))
     )
             print(agency.text)
             amount = WebDriverWait(content, 10).until(
                 EC.presence_of_element_located((By.XPATH, './div/div/div/div[1]/a/span[2]'))
     )
             print(amount.text)
             
             Table_dict={ 'Agency': agency.text,
                    'Amount': amount.text} 
             list.append(Table_dict) 
             df = pd.DataFrame(list)
     
  
             df.to_csv('agencies1.csv') 


#table 
try:
    element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="bs-example-navbar-collapse-1"]/ul[2]/li[1]/a'))
    )
    element.click()
    element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "National Science Foundation"))
    )
    element.click()

except:
     driver.quit()
time.sleep(10)

#find table
table=driver.find_element_by_xpath('//*[@id="investments-table-object_wrapper"]/div[3]').text

# print(table)

time.sleep(5)
n=1
tablelist = [] 
while(1): 
    try:

        row1=driver.find_element_by_xpath('//*[@id="investments-table-object"]/tbody/tr['+str(n)+']/td[1]').text 
        row2=driver.find_element_by_xpath('//*[@id="investments-table-object"]/tbody/tr['+str(n)+']/td[2]').text  
        row3=driver.find_element_by_xpath('//*[@id="investments-table-object"]/tbody/tr['+str(n)+']/td[3]').text  
        row4=driver.find_element_by_xpath('//*[@id="investments-table-object"]/tbody/tr['+str(n)+']/td[4]').text  
        row5=driver.find_element_by_xpath('//*[@id="investments-table-object"]/tbody/tr['+str(n)+']/td[5]').text  
        row6=driver.find_element_by_xpath('//*[@id="investments-table-object"]/tbody/tr['+str(n)+']/td[6]').text  
        row7=driver.find_element_by_xpath('//*[@id="investments-table-object"]/tbody/tr['+str(n)+']/td[7]').text  

        Table_data={ 'UII': row1,
                    'Bureau': row2,
                    'Investment Title': row3,
                    'Total FY2021 Spending ($M)': row4,
                    'Type': row5,
                    'CIO Rating': row6,
                    '# of Projects': row7,}
        
        tablelist.append(Table_data) 
        tl = pd.DataFrame(tablelist)

        n += 1
    except NoSuchElementException: 
        break
          
tl.to_csv('table.csv') 



numberOfRows = len(driver.find_elements_by_xpath('//*[@id="investments-table-object"]/tbody/tr'))
for iRow in range(numberOfRows):
    element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="investments-table-object"]/tbody/tr['+str(iRow+1)+']/td[1]/a'))
        )
    element.click()
    element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Download Business Case PDF"))
        )
    element.click()
    driver.back()
    time.sleep(10)
    driver.back()
    # print(numberOfRows)
