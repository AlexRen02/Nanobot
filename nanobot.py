# Import Module
import random
import datetime
import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

# Login
def login(driver):
    # User Input Login Info
    username = input("Username:")
    password = getpass.getpass("Password:")

    # Locate login buttons and inputs
    login_open_button = driver.find_element_by_id('ihm_login_button')
    user_box = driver.find_element_by_id('name')
    pass_box = driver.find_element_by_id('pw')
    login_button = driver.find_element_by_id('login_form_button')

    # Open Login Window and Log In
    time.sleep(1)
    login_open_button.click()
    time.sleep(1)
    user_box.send_keys(username)
    pass_box.send_keys(password)
    login_button.click()

# Faucet Claim
def faucet_claim(driver):
    # Current ticket amount
    ticket_total = driver.find_element_by_xpath('//*[@id="bonus_accumulated"]/span').get_attribute('innerHTML')

    # Claim tickets if faucet full
    if ticket_total == '20/20':
        # Faucet Window Buttons
        faucet_button = driver.find_element_by_id('ihm_faucet_button')
        claim_button = driver.find_element_by_id('bonus_claim')

        faucet_button.click()
        time.sleep(1)
        claim_button.click()

# Lottery Claim
def lottery_claim(driver, last, lotto_total):
    now = datetime.datetime.now() # Current time
    time_in_hours = (now - last).total_seconds()/3600 # Difference between current time and last claim in hours

    # If lottery claim requirements met, claim lottery ticket
    if time_in_hours >= 1 and lotto_total < 10:
        send_chat(driver, 'lotto') # Send chat to claim lottery
        lotto_total += 1 # Lottery tickets increased by 1
        return now, lotto_total # Return current time and new lottery total
    
    return last, lotto_total # Return last claim time and lottery total

# Send Chat
def send_chat(driver, chat):
    chat_box = driver.find_element_by_xpath('//*[@id="chat-input"]')
    chat_box.send_keys(chat + Keys.ENTER)

def main():
    # Website URL
    url = 'https://luckynano.com/?p=index'
    dice = 'https://luckynano.com/?p=dice'

    # Open Chrome
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Open URL    
    driver.get(url)

    # Wait for page to load
    time.sleep(1)

    # Home Page Button
    home_page = driver.find_element_by_xpath('//*[@id="home_logo"]')

    # Time Variables
    last = datetime.datetime(2000, 1, 1) # Last lottery ticket collection time

    # Initialize lotto ticket total
    lotto_total = 0

    # Dice Roll Variables
    my_tickets = 0
    ticket_bet = '1'
    ticket_payout = '10'
    #nano_bet = 0.001
    #nano_payout = 3

    # Login
    login(driver)

    while True:
        # Claim faucet
        time.sleep(5)
        faucet_claim(driver)

        # Claim lottery ticket if possible and set new last claim time and lottery ticket total
        time.sleep(5)
        last, lotto_total = lottery_claim(driver, last, lotto_total)

        # Auto dice roll
        my_tickets = int(driver.find_element_by_xpath('//*[@id="header_silver_count"]/span').get_attribute('innerHTML'))
        if my_tickets > 0:
            # Dice Roll Page
            dice_page = driver.find_element_by_xpath('//*[@id="header_content"]/div[4]/div[2]')
            time.sleep(1)

            # Go to dice page
            dice_page.click()
            time.sleep(5)

            # Dice page buttons
            dice_bet_input = driver.find_element_by_xpath('//*[@id="dice_manual_bet"]/input')
            dice_payout_input = driver.find_element_by_xpath('//*[@id="dice_manual_payout"]/input')
            roll_under_button = driver.find_element_by_xpath('//*[@id="dice_manual_roll_low"]')
            roll_over_button = driver.find_element_by_xpath('//*[@id="dice_manual_roll_high"]')

            while my_tickets != 0:
                time.sleep(5)

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
        time.sleep(2)
        if driver.current_url != url:
            home_page.click()
            time.sleep(5)

if __name__ == '__main__':
    main()