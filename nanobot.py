# Import Module
import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

# Website URL
url = 'https://luckynano.com/?p=signin'

# User Input Login Info
username = input("Username:")
password = getpass.getpass("Password:")

# Open Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open URL    
driver.get(url)

# Wait for page to load
time.sleep(1)

# Login
# Login Buttons and Inputs
login_open_button = driver.find_element_by_id('ihm_login_button')
user_box = driver.find_element_by_id('name')
pass_box = driver.find_element_by_id('pw')
login_button = driver.find_element_by_id('login_form_button')

# Open Login Window and Log In
login_open_button.click()
user_box.send_keys(username)
pass_box.send_keys(password)
login_button.click()

# Claim faucet
# Faucet Window Buttons
faucet_button = driver.find_element_by_id('ihm_faucet_button')
claim_button = driver.find_element_by_id('bonus_claim')

# Wait for data to load
time.sleep(1)

# Current ticket amount
ticket_total = driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[10]/div/div[2]/div[1]/span').get_attribute('innerHTML')

# Claim tickets if tickets are full
if ticket_total == '20/20':
    faucet_button.click()
    claim_button.click()