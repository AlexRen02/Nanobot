# Import Module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# open Chrome
driver = webdriver.Chrome(
    '"C:\Users\renal\Downloads\chromedriver_win32\chromedriver.exe"')

# Open URL
driver.get('https://luckynano.com/?p=index')
print(driver.page_source)