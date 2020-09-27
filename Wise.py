#ivri korem 2020
"""
Description
"""
#import
from SideFiles.Utilities import SelHelper
from SideFiles.Utilities.SelHelper import SelHelper
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import os
import random
import time
import pandas as pd

#Welcoming
print("")

#Getting Input from the user
WebBrowser = input("What browser do you use? ").lower()
searchTarget = input("What do you want to search? ")


#Init
if WebBrowser == "chrome":
    DriverLocation = "the path to the 'chromedriver' in the repo"
    os.environ["webdriver.chrome.driver"] = DriverLocation
    driver = webdriver.Chrome(executable_path=DriverLocation)
elif WebBrowser == "firefox":
    driver = webdriver.Firefox(executable_path="the path to the 'geckodriver' in the repo")

sel = SelHelper(driver)
data =[["article","MLA","APA", "Chicago"]]

#Entering the target site
driver.get("https://scholar.google.com")
driver.maximize_window()
driver.implicitly_wait(5)

#search subject or author based on user input
searchBar = sel.getElement('//*[@id="gs_hdr_tsi"]')
searchBar.send_keys(searchTarget)
searchButton = sel.getElement("/html//button[@id='gs_hdr_tsb']").click()
comp = 0

#get the articles elements
articles = driver.find_elements(By.XPATH, "/html/body/div/div[10]/div[2]/div[2]/div[2]/div/div[2]/h3/a")
citeButtons = driver.find_elements(By.XPATH, '/html/body/div/div[10]/div[2]/div[2]/div[2]//a[@class="gs_or_cit gs_nph"]')
articleNames = []
for article in articles:
    articleNames.append(article.text)

#iterate through the articles with a loop
for button in citeButtons:
    #click the site icon get all the cites in a list and push that list to "data"
    button.click()
    time.sleep(0.5)
    citeElements = driver.find_elements(By.XPATH, '/html/body/div/div[4]/div/div[2]/div/div[1]/table/tbody/tr//div')
    cites = []
    for element in citeElements:
        cites.append(element.text)
    cites.insert(0, articleNames[comp])
    data.append(cites)

    sel.getElement('gs_cit-x', "id").click()
    #raise the comparison
    if comp <8 :
        comp += 1

#convert "data" to csv with pandas
df = pd.DataFrame(data)
df.to_csv('cites.csv', index = False, header = False)