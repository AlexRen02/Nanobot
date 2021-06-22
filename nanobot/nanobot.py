# Import Module
import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

# website URL
url = 'https://luckynano.com/?p=signin'

# Login Info
username = input("Username:")
password = getpass.getpass("Password:")

# Open Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open URL    
driver.get(url)

# Wait for page to load
time.sleep(5)

# Log In
login_open_button = driver.find_element_by_id('ihm_login_button')
user_box = driver.find_element_by_id('name')
pass_box = driver.find_element_by_id('pw')
login_button = driver.find_element_by_id('login_form_button')

login_open_button.click()
user_box.send_keys(username)
pass_box.send_keys(password)
login_button.click()