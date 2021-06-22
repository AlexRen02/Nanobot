# Import Module
import datetime
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
time.sleep(1)
user_box.send_keys(username)
pass_box.send_keys(password)
login_button.click()

# Faucet Window Buttons
faucet_button = driver.find_element_by_id('ihm_faucet_button')
claim_button = driver.find_element_by_id('bonus_claim')

# Chat
time.sleep(1)
chat_box = driver.find_element_by_xpath('/html/body/div[1]/div[5]/form/textarea')

# Initialize Time Variables
reset = datetime.datetime(2100, 1, 1, 11) # Lottery reset time
last = datetime.datetime(2000, 1, 1) # Last lottery ticket collection time
now = datetime.datetime.now() # Current time
# Initialize lotto ticket total
lotto = 0

while True:
    # Wait for data to load
    time.sleep(1)

    # Claim faucet
    # Current ticket amount
    ticket_total = driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[10]/div/div[2]/div[1]/span').get_attribute('innerHTML')

    # Claim tickets if tickets are full
    if ticket_total == '20/20':
        faucet_button.click()
        time.sleep(1)
        claim_button.click()
        time.sleep(1)

    # Difference in time between now and last collection
    diff = (now - last).total_seconds()/3600

    # Claim lotto ticket
    if lotto < 10 and diff >= 1:
        chat_box.send_keys('lotto' + Keys.ENTER)
        last = now
        now = datetime.datetime.now()
        lotto += 1

