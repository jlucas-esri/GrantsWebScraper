import logging
from scraper.htmlRetriever import HtmlRetriever
from selenium import webdriver
from scraper.iterateGrantItems import IterateGrantItems
import time
from scraper.iteratePages import IteratePages
import json


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
    time.sleep(2)
    
    #set initial settings for what is to be scraped
    pageNum = 0
    allItemsData = []
    try:
        for page in IteratePages(driver):
            pageNum += 1
            logger.info(f'Navigated to page {pageNum}')
            itemsData = IterateGrantItems(page).iterateAndGetInfo()
            allItemsData.extend(itemsData)
    except KeyboardInterrupt as e:
        logger.error('Process canceled. Saving data to the nearest page.')

    #storing the items data
    with open('data.json', 'w') as f:
        json.dump(allItemsData, f)

if __name__ == '__main__':
    main()