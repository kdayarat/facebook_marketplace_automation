from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

LOGIN_URL = 'https://www.facebook.com/login.php'
KEYWORD = 'monitor' # Changes this to change the search parameter

class FacebookLogin():
    def __init__(self, email, password, browser='Chrome'):
        # Store credentials for login
        self.email = email
        self.password = password
        if browser == 'Chrome':
            # Use chrome, disable notifications
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications":2}
            chrome_options.add_experimental_option("prefs",prefs)
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), port = 0, options = chrome_options)
        elif browser == 'Firefox':
            # Set it to Firefox
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        self.driver.get(LOGIN_URL)
        time.sleep(1)
    
    def login(self):
        email_element = self.driver.find_element_by_id('email')
        email_element.send_keys(self.email) # Give keyboard input 

        password_element = self.driver.find_element_by_id('pass')
        password_element.send_keys(self.password) # Give password

        login_button = self.driver.find_element_by_id('loginbutton')
        login_button.click() # Send mouse click

        time.sleep(2)

    def browseMarketplace(self):
        marketplace_button = self.driver.find_element_by_xpath("//a[@href='/marketplace/?ref=app_tab']")
        marketplace_button.click()

        time.sleep(1)
        self.driver.implicitly_wait(5)

        search_element = self.driver.find_element_by_xpath('//input[@aria-label="Search Marketplace"]')
        # KEYWORD = input("Enter search terms: ")
        search_element.send_keys(KEYWORD)
        search_element.send_keys(Keys.RETURN)

        used_item_links = []

        for i in range(5):
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
            except:
                pass
        
            items_list = self.driver.find_elements_by_xpath('//div[@aria-label="Collection of Marketplace items"]')
            if used_item_links == 0:
                used_item_links = [item.get_attribute('href') for item in items_list]
            else:
                used_item_links.append([item.get_attribute('href') for item in items_list])
        
            print([item.get_attribute('href') for item in items_list])
        
        print(used_item_links)

if __name__ == '__main__':
    fb_login = FacebookLogin(email='bobs19690@gmail.com', password='J3b_84173D', browser='Chrome')
    fb_login.login()
    fb_login.browseMarketplace()

