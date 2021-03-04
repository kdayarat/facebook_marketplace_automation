from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import yaml
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
            chrome_options.add_argument("--start-maximized")
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

    def removeListing(self):
        self.driver.implicitly_wait(5)

        marketplace_button = self.driver.find_element_by_xpath("//a[@href='https://www.facebook.com/marketplace/?ref=bookmark']")
        marketplace_button.click()
        self.driver.implicitly_wait(5)

        marketplace_account = self.driver.find_element_by_xpath("//*[text()='Your Account']")
        marketplace_account.click()
        self.driver.implicitly_wait(5)

        stream = open('adInfo.yaml')
        ad_info = yaml.load(stream, Loader=yaml.FullLoader)

        ad_title = ad_info.get("title") # Gets the title of the ad that is to be deleted
        ad_button = self.driver.find_element_by_xpath("//div[@aria-label='"+ad_title+"']")
        ad_button.click() # Clicks on the specific ad

        self.driver.find_element_by_xpath("//div[@aria-label='Delete']").click() # Initial delete button
        self.driver.find_element_by_xpath("//*[text()='Delete']").click() # Confirmation of deletion

        # self.driver.find_element_by_xpath("//div[@aria-label='More']").click() # More options drop down menu
        # self.driver.find_element_by_xpath("//*[text()='Delete Listing']").click() # Initial delete button
        # time.sleep(1)
        # self.driver.find_element_by_xpath("//div[@aria-label='Delete']").click() # Confirmation of deletion

        
if __name__ == '__main__':
    fb_login = FacebookLogin(email='bobs19690@gmail.com', password='J3b_84173D', browser='Chrome')
    fb_login.login()
    fb_login.removeListing()
