import logging
from scraper.htmlRetriever import HtmlRetriever
from selenium import webdriver
from scraper.iterateGrantItems import IterateGrantItems
import time


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():

    driver = webdriver.Chrome(executable_path=r'resources/chromedriver.exe') 
    initialLink = r'https://www.grants.gov/web/grants/search-grants.html'

    driver.get(initialLink)
    
    #set initial settings for what is to be scraped

    IterateGrantItems(driver).iterateAndGetInfo()

    time.sleep(5)

if __name__ == '__main__':
    main()