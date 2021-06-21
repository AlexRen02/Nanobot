# Import Module
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

url = 'https://luckynano.com/?p=index'

# open Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open URL    
driver.get(url)

# Wait for page to load
time.sleep(5)

