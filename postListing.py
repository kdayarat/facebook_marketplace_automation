from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import yaml
import pyautogui
import time
import os

LOGIN_URL = 'https://www.facebook.com/login.php'

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

    def postListing(self):
        self.driver.implicitly_wait(5)

        create_button = self.driver.find_element_by_xpath("//div[@aria-label='Create']")
        create_button.click() 

        self.driver.implicitly_wait(5)

        create_listing_button = self.driver.find_element_by_xpath("//a[@href='/marketplace/create/item/']")
        create_listing_button.click() #Clicks create add button

        self.driver.implicitly_wait(5)
        
        # root_node = ET.parse('adInfo.xml').getroot() # Parses the XML file containing the ad information

        stream = open('adInfo.yaml')
        ad_info = yaml.load(stream, Loader=yaml.FullLoader)

        ad_title = ad_info.get("title")
        title_element = self.driver.find_element_by_xpath("//label[@aria-label='Title']")
        title_element.send_keys(ad_title) # Types in title of ad

        ad_price = ad_info.get("price")
        price_element = self.driver.find_element_by_xpath("//label[@aria-label='Price']")
        price_element.send_keys(ad_price) #  Types in price

        category_button = self.driver.find_element_by_xpath("//label[@aria-label='Category']")
        category_button.click()
        ad_category = ad_info.get("category")
        category_path = "//*[text()='"+ad_category+"']" 
        category = self.driver.find_element_by_xpath(category_path) 
        category.click() # selects appropriate catagory from menu

        condition_button = self.driver.find_element_by_xpath("//label[@aria-label='Condition']")
        condition_button.click()
        ad_condition = ad_info.get("condition")
        condition_path = "//*[text()='"+ad_condition+"']" 
        condition = self.driver.find_element_by_xpath(condition_path)
        condition.click() # selects appropriate condition from the four options

        ad_description = ad_info.get("description")
        description_element = self.driver.find_element_by_xpath("//label[@aria-label='Description']")
        description_element.send_keys(ad_description) # types in description

        location_element = self.driver.find_element_by_xpath("//label[@aria-label='Location']")
        ad_location = ad_info.get("location")
        location_element.send_keys(ad_location)
        location_path = "//*[text()='"+ad_location+"']" 
        location = self.driver.find_element_by_xpath(location_path)
        location.click() # adds location
     
        image_search = self.driver.find_element_by_xpath("//div[@aria-label='Add Photos']")

        for tag in ad_info.get("images"):
            image_search.click()
            image_path = '"'+os.getcwd()+"\\images\\"+tag+'" ' # Finds the path for each image
            time.sleep(2)
            pyautogui.write(image_path)
            pyautogui.press('enter') # uploads the image
            image_search = self.driver.find_element_by_xpath("//div[@aria-label='Add Photo']")
            time.sleep(2)
     
        self.driver.implicitly_wait(10)
        time.sleep(2)

        next_button = self.driver.find_element_by_xpath("//div[@aria-label='Next']")
        next_button.click()
        time.sleep(2)
        post_button = self.driver.find_element_by_xpath("//div[@aria-label='Publish']")
        post_button.click() # publishes ad
        

if __name__ == '__main__':
    # fb_login = FacebookLogin(email='vsb10774@bcaoo.com', password='uw4thewin!!', browser='Chrome')
    fb_login = FacebookLogin(email='bobs19690@gmail.com', password='J3b_84173D', browser='Chrome')
    fb_login.login()
    fb_login.postListing()

