"""install.py - Install WebDriver for chrome"""

from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install()))
