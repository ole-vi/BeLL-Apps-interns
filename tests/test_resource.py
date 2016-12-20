import unittest
import bell

from base_case import on_platforms
from base_case import browsers
from base_case import BaseCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
from random import choice
from string import ascii_lowercase

@on_platforms(browsers)
class ResourceTest(BaseCase):

#    Add New Resource - DONE
#TODO: Think of a better test to check if resource was added successfully.

#    Request Resource - DONE
#    Add 2 Collections
#    Add New Resource to Collection
#    Merge Collections
#    Delete Resource
#    Delete Collections

    def test_add_resource(self):
        driver = self.driver
        self.setup_library()
        
        # add new resource
        button = driver.find_element_by_id("addNewResource")
        button.click()
        
        # test add resource page is reached
        expected = bell.get_url() + "#resource/add"
        actual = driver.current_url
        self.assertEqual(actual, expected)
        sleep(3)
        
        # fill out new resource form
        fill = "ole"
        fill = self.new_resource_form(fill)
        
        # test form successfully submitted
        sleep(10)
        elem = driver.find_element_by_xpath("//*[@id='parentLibrary']//table/tbody/tr/td[./p[contains(text(), '"+fill+"')]]")
        if fill in elem.text:
            actual = True
        expected = True
        self.assertEqual(actual, expected)

    def new_resource_form(self, fill):
        driver = self.driver
        fields = ["title", "author", "Publisher", "linkToLicense"]
        for field in fields:
            elem = driver.find_element_by_name(field)
            elem.clear()
            elem.send_keys(fill)
        
        elem = driver.find_element_by_name("Year")
        elem.clear()
        elem.send_keys("2016")
        
        select = Select(driver.find_element_by_name("language"))
        select.select_by_value("English")
        
        elem_list = driver.find_elements_by_xpath("//*[contains(text(), 'Select an Option')]")
        for i in range(len(elem_list)):
            elem_list[i].click()
            elem_list[i].send_keys(Keys.RETURN)
        
        # save resource
        button = driver.find_element_by_name("save")
        button.click()
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "addNewResource")))
        except:
            if Alert(driver) and Alert(driver).text == "Title already exists.":
                Alert(driver).accept()
                self.new_resource_form("".join(choice(ascii_lowercase) for i in range(3)))
        return fill                 

#    def test_request_resource(self):
#        driver = self.driver
#        self.setup_library()
#        
#        # access request form
#        button = driver.find_element_by_id("requestResource")
#        button.click()
#        # fill out form
#        elem = driver.find_element_by_name("request")
#        elem.send_keys("test")
#        # submit form
#        button = driver.find_element_by_xpath("//*[@id='formButton']")
#        button.click()
#        
#        # test alert
#        actual = Alert(driver).text
#        expected = "Request successfully sent."
#        self.assertEqual(actual, expected)
#        Alert(driver).accept()
#        
#        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "requestResource")))
#        
#        # test it's actually there
#        button = driver.find_element_by_id("requestResource")
#        button.click()
#        # view all requests
#        button = driver.find_element_by_xpath("//*[contains(text(), 'View All')]")
#        button.click()
#        # find submitted resource
#        actual = False
#        elem = driver.find_element_by_id("requestsTable")
#        rows = elem.find_elements_by_tag_name("tr")
#        for row in rows:
#            if row.find_element_by_tag_name("td")[2].text == "test":
#                actual = True
#        expected = True
#        self.assertEqual(actual, expected)
#        
#    def test_new_collection(self):
#        driver = self.driver
#        self.setup_library()
#        
#        # switch to collections
#        elem = driver.find_element_by_xpath("//*[@id='labelOnResource']")
#        link = elem.find_element_by_link_text("Collections")
#        link.click()

        
    def setup_library(self):
        driver = self.driver
        
        # login
        bell.login(driver, "admin", "password")
        
        # go to library
        library = driver.find_element_by_link_text("Library")
        library.click()
        
        # test resource page is reached
        expected = bell.get_url() + "#resources"
        actual = driver.current_url
        self.assertEqual(actual, expected)
        sleep(5)

if __name__ == "__main__":
    unittest.main()
