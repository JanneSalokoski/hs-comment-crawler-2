"""crawler.py - Provide a selenium crawler to get hs-comments"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains as AC


TIMEOUT = 1

class Crawler:
    """Provide a crawler Class for the script"""
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.actions = AC(self.driver)

    def load_page(self, url):
        """Load a page"""
        self.driver.get(url)

    def get_element_by_query(self, query):
        """Find an element by css-query"""
        return self.driver.find_element(By.CSS_SELECTOR, query)

    def get_elements_by_query(self, query):
        """Find elements by css-query"""
        return self.driver.find_elements(By.CSS_SELECTOR, query)

    def wait_for_element_condition_by_query(self, query, condition, timeout=TIMEOUT):
        """Wait for element to meet a condition by query"""
        try:
            element = WebDriverWait(self.driver, timeout=timeout).until(
                condition((By.CSS_SELECTOR, query))
            )

            return element
        except:
            print(f"Element not found by query '{query}'")
            return None

    def wait_for_element_presence_by_query(self, query, timeout=TIMEOUT):
        """Wait for element to be present by query"""
        return self.wait_for_element_condition_by_query(query, EC.presence_of_element_located, timeout)

    def wait_for_element_clickable_by_query(self, query, timeout=TIMEOUT):
        """Wait for element to be clickable by query"""
        return self.wait_for_element_condition_by_query(query, EC.element_to_be_clickable, timeout)

    def switch_to_frame(self, query):
        """Switch to an iframe by selector"""
        self.driver.switch_to.frame(self.wait_for_element_presence_by_query(query))

    def switch_back(self):
        """Switch back to default frame"""
        self.driver.switch_to.default_content()

    def move_to_element(self, element):
        """Move to an existing element"""
        self.actions.move_to_element(element).perform()

    def scroll_by_pixels(self, pixels):
        """Scroll by a pixel amount"""
        self.driver.execute_script(f"window.scrollBy(0, {pixels})")

    def click_by_js_query(self, query):
        """Click an element with javascript"""
        try:
            self.driver.execute_script(f"document.querySelector('{query}').click();")
            print(f"Element found by query '{query}'")
            return True
        except:
            #print(f"Element not found by query '{query}'")
            return False
