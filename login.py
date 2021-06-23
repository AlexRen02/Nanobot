# Import Module
import getpass
import time

# Login
def login(driver):
    # User Input Login Info
    username = input("Username:")
    password = getpass.getpass("Password:")

    # Login Buttons and Inputs
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

