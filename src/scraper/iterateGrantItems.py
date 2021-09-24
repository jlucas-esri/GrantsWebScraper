import logging
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class IterateGrantItems:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    def __init__(self, driver):
        self.driver = driver
        self.iframe = self.driver.find_element_by_css_selector('iframe#embeddedIframe')
        self.driver.switch_to.frame(self.iframe)

    def _iterateThroughListOfElements(self, listOfElements, listOfElementsId:str):
        for resultIdx in range(len(listOfElements)):
            searchResultsDiv = self.driver.find_element_by_id('searchResultsDiv')
            results = searchResultsDiv.find_elements_by_class_name(listOfElementsId)
            self.logger.debug(f'length of results for {listOfElementsId}: {len(results)}')
            result = results[resultIdx]
            detailsLink = result.find_element_by_css_selector("a[title=\"Click to View Grant Opportunity\"]")
            detailsLink.click()
            
            time.sleep(5)

            #go back to previous page
            self.driver.execute_script("window.history.go(-1)")
            # while True:
            #     pass
            time.sleep(0.3)
            self.driver.switch_to.default_content()
            self.driver.switch_to_frame('embeddedIframe')
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'searchResultsDiv')))


    def iterateAndGetInfo(self):
        """
        Finds all the links associated with detail pages and navigates to them
        """
        searchResultsDiv = self.driver.find_element_by_id('searchResultsDiv')
        self.logger.debug('past getting table div')


        #getting all visible grants on page
        resultsEvenList = searchResultsDiv.find_elements_by_class_name('gridevenrow')
        resultsOddList = searchResultsDiv.find_elements_by_class_name('gridoddrow')
        self.logger.debug('past getting list of results')

        #acting on each grant
        self.logger.debug('acting on each grant')

        self._iterateThroughListOfElements(resultsEvenList, 'gridevenrow')
        self._iterateThroughListOfElements(resultsOddList, 'gridoddrow')