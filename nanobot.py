# Import Module
import random
import datetime
import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

# Website URL
url = 'https://luckynano.com/?p=index'
dice = 'https://luckynano.com/?p=dice'

# User Input Login Info
username = input("Username:")
password = getpass.getpass("Password:")

# Open Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open URL    
driver.get(url)

# Wait for page to load
time.sleep(1)

# Home Page Button
home_page = driver.find_element_by_xpath('//*[@id="home_logo"]')

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

# Time Variables
last = datetime.datetime(2021, 6, 22, 14, 15) # Last lottery ticket collection time

# Initialize lotto ticket total
lotto = 0

# Dice Roll Variables
my_tickets = 0
ticket_bet = '1'
ticket_payout = '10'
#nano_bet = 0.001
#nano_payout = 3

# Dice Roll Page
dice_page = driver.find_element_by_xpath('//*[@id="header_content"]/div[4]/div[2]')

while True:

    time.sleep(1)

    # Claim faucet
    # Current ticket amount
    ticket_total = driver.find_element_by_xpath('//*[@id="bonus_accumulated"]/span').get_attribute('innerHTML')

    # Claim tickets if tickets are full
    if ticket_total == '20/20':
        # Faucet Window Buttons
        faucet_button = driver.find_element_by_id('ihm_faucet_button')
        claim_button = driver.find_element_by_id('bonus_claim')

        faucet_button.click()
        time.sleep(1)
        claim_button.click()
        time.sleep(1)

    # Difference in time between now and last collection
    now = datetime.datetime.now()
    diff = (now - last).total_seconds()/3600

    # Claim lotto ticket
    if lotto < 10 and diff >= 1:
        # Chat
        chat_box = driver.find_element_by_xpath('//*[@id="chat-input"]')
        chat_box.send_keys('lotto' + Keys.ENTER)
        last = now
        now = datetime.datetime.now()
        lotto += 1

    # Auto dice roll
    my_tickets = int(driver.find_element_by_xpath('//*[@id="header_silver_count"]/span').get_attribute('innerHTML'))
    if my_tickets > 0:
        # Go to dice page
        dice_page.click()
        time.sleep(1)

        # Dice page buttons
        dice_bet_input = driver.find_element_by_xpath('//*[@id="dice_manual_bet"]/input')
        dice_payout_input = driver.find_element_by_xpath('//*[@id="dice_manual_payout"]/input')
        roll_under_button = driver.find_element_by_xpath('//*[@id="dice_manual_roll_low"]')
        roll_over_button = driver.find_element_by_xpath('//*[@id="dice_manual_roll_high"]')

        while my_tickets != 0:
            time.sleep(2)

            # Send dice info
            dice_bet_input.send_keys(Keys.CONTROL, 'a') 
            dice_bet_input.send_keys(ticket_bet)
            dice_payout_input.send_keys(Keys.CONTROL, 'a')
            dice_payout_input.send_keys(ticket_payout)

            # Randomly select roll under or roll over
            # To be changed
            x = random.random()
            if x < 0.5:
                roll_over_button.click()
            else:
                roll_under_button.click()
        
            # New ticket amount
            time.sleep(1)
            my_tickets = int(driver.find_element_by_xpath('//*[@id="header_silver_count"]/span').get_attribute('innerHTML'))

    # Return to home page if not rolling
    if driver.current_url != url:
        home_page.click()