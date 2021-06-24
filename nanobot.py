# Import Module
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import random
import datetime
import getpass
import time

# Login
def login(url):
    # User Input Login Info
    username = input("Username:")
    password = getpass.getpass("Password:")

    # Open Chrome
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Open URL    
    driver.get(url)

    # Wait for page to load
    time.sleep(1)

    # Locate login buttons and inputs
    login_open_button = driver.find_element_by_id('ihm_login_button')
    user_box = driver.find_element_by_id('name')
    pass_box = driver.find_element_by_id('pw')
    login_button = driver.find_element_by_id('login_form_button')

    # Open Login Window and Log In
    time.sleep(1)
    login_open_button.click()
    user_box.send_keys(username)
    pass_box.send_keys(password)
    login_button.click()

    # Return driver
    return driver

# Faucet Claim
def faucet_claim(driver):
    # Current ticket amount
    ticket_total = driver.find_element_by_xpath('//*[@id="bonus_accumulated"]/span').get_attribute('innerHTML')

    # Claim tickets if faucet full
    if ticket_total == '20/20':
        # Faucet Window Buttons
        faucet_button = driver.find_element_by_id('ihm_faucet_button')
        claim_button = driver.find_element_by_id('bonus_claim')

        time.sleep(1)
        faucet_button.click()
        claim_button.click()

# Lottery Claim
def lottery_claim(driver, next_ticket, lotto_total):
    # If lottery claim requirements met, claim lottery ticket
    if next_ticket == True and lotto_total < 10:
        send_chat(driver, 'lotto') # Send chat to claim lottery
        lotto_total += 1 # Lottery tickets increased by 1
    
    return lotto_total # Return lottery ticket total

# Send Chat
def send_chat(driver, chat):
    # Find chat box
    chat_box = driver.find_element_by_xpath('//*[@id="chat-input"]')
    
    # Send chat
    chat_box.send_keys(chat + Keys.ENTER)

# Play Dice
def play_dice(driver, url, bet, payout):
    my_tickets = int(driver.find_element_by_xpath('//*[@id="header_silver_count"]/span').get_attribute('innerHTML'))
    if my_tickets > 0:
        driver.get(url)
        time.sleep(5)

        # Dice page buttons
        dice_bet_input = driver.find_element_by_xpath('//*[@id="dice_manual_bet"]/input')
        dice_payout_input = driver.find_element_by_xpath('//*[@id="dice_manual_payout"]/input')
        roll_under_button = driver.find_element_by_xpath('//*[@id="dice_manual_roll_low"]')
        roll_over_button = driver.find_element_by_xpath('//*[@id="dice_manual_roll_high"]')

        while my_tickets > 0:
            # Send dice info
            dice_bet_input.send_keys(Keys.CONTROL, 'a') 
            dice_bet_input.send_keys(bet)
            dice_payout_input.send_keys(Keys.CONTROL, 'a')
            dice_payout_input.send_keys(payout)

            # Select dice roll and roll
            if select_roll() == 'over':
                roll_over_button.click()
            else:
                roll_under_button.click()

            # Get new ticket amount
            time.sleep(1)
            my_tickets = int(driver.find_element_by_xpath('//*[@id="header_silver_count"]/span').get_attribute('innerHTML'))

# Dice roll selection
def select_roll():
    # Currently random selection
    # To be changed
    x = random.random()
    if x < 0.5:
       return 'over'
    else:
        return 'under'

# Returns if next lottery ticket is available
def ticket_check(driver):
    send_chat(driver, '/lottery')
    time.sleep(2)
    substring = 'Next ticket available in'
    text = driver.find_element_by_xpath('(//*[@id="chat-box"]/p[@class="chat_system_message"])[last()]').get_attribute('innerHTML')
    if substring in text:
        return False
    return True

def main():
    # Website URL
    home = 'https://luckynano.com/?p=index'
    dice = 'https://luckynano.com/?p=dice'

    # Dice Roll Variables
    ticket_bet = '1'
    ticket_payout = '10'
    #nano_bet = 0.001
    #nano_payout = 3
    
    # Login and set webdriver
    driver = login(home)
    time.sleep(1)
    
    # Find lotto_total
    send_chat(driver, '/lottery')
    time.sleep(1)
    lotto_total = int(driver.find_element_by_xpath('(//*[@id="chat-box"]/p[@class="chat_system_message"])[last()-1]/span').get_attribute('innerHTML'))
    
    # Main loop
    while True:
        # Claim faucet
        time.sleep(2)
        faucet_claim(driver)

        # Claim lottery ticket if possible and set new last claim time and lottery ticket total
        time.sleep(2)
        next_ticket = ticket_check(driver)
        lotto_total = lottery_claim(driver, next_ticket, lotto_total)

        # Auto dice roll
        time.sleep(2)
        play_dice(driver, dice, ticket_bet, ticket_payout)

        # Return to home page if not playing
        if driver.current_url != home:
            driver.get(home)
            time.sleep(5)

if __name__ == '__main__':
    main()