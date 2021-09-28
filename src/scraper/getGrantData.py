from scraper.htmlRetriever import HtmlRetriever
import re
from pprint import pprint
from bs4 import BeautifulSoup
import logging

class GetGrantData:

    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlRetriever.main(driver)
        self.soup = BeautifulSoup(self.html, 'html.parser')

    @staticmethod
    def run(driver) -> dict:
        """
        Gets all necessary data from the grant entry pages and returns it as a dict

        Args:
            driver: the selenium webdriver that has already navigated to a grant entry page

        Returns:
            dict: containing all of the necessary data from that grant entry
        """

        dataObj = GetGrantData(driver)
        data = dataObj._getSynopsisInfo(dataObj.soup)
        return data

    
    def _getSynopsisInfo(self, soup: BeautifulSoup) -> dict:
        """
        Getting all the info on the synopsis grant page
        
        Args:
            soup: the html of the synopsis grant page

        Returns:
            dict: containing all of the data from the synopsis grant page
        """
        synopsisData = {}
        #getting general info
        synopsisData.update({'general': self._getGeneralInfo(soup)})

        #getting eligibility info
        synopsisData.update({'eligibility': self._getEligibilityInfo(soup)})

        #getting additional info
        synopsisData.update({'additional': self._getAdditionalInfo(soup)})

        pprint(synopsisData)
        return synopsisData

    def _recordEntries(self, entries) -> dict:
        infoDict = {}
        #looping through the entries in each container
        for entry in entries:
            labelTextDirty = entry.find('th').get_text()
            labelTextClean = re.sub(r':', r'', labelTextDirty)
            valueText = entry.find('span').get_text()

            #cleaning up the "empty" values on the webpage
            valueText = re.sub(r'(\xa0)', '', valueText)

            #adding the entry label and entry value to a dict
            infoDict.update({labelTextClean: valueText})
        return infoDict



    def _getGeneralInfo(self, container) -> dict:
        """
        Getting the info from the general section on the synopsis page

        Args:
            container: the section of html that contains the necessary elements. 
                       In this case, the entire html document is passed as a
                       BeautifulSoup instance

        Returns:
            dict: the data pulled from the general section of the website.

        Raises:
            RuntimeError: if any unexpected state is found during web scraping
        """
        #getting containers
        containerLeft = container.find(id='synopsisDetailsGeneralInfoTableLeft')
        containerRight = container.find(id='synopsisDetailsGeneralInfoTableRight')

        if containerLeft.find('tr') is None and containerRight.find('tr') is None:
            containerLeft = container.find(id='forecastDetailsGeneralInfoTableLeft')
            containerRight = container.find(id='forecastDetailsGeneralInfoTableRight')

        if containerLeft is None or containerRight is None:
            raise RuntimeError('One or both of the containers are empty.')
        infoDict = {}
        #looping through the containers
        for sideContainer in [containerLeft, containerRight]:
            # table = sideContainer.find('table', cellpadding='5')
            entries = sideContainer.find_all('tr')
            if not len(entries):
                raise RuntimeError('No data entries')

            infoDict.update(self._recordEntries(entries))   

        if not len(infoDict):
            raise RuntimeError('General info is empty')

        return infoDict


    def _getEligibilityInfo(self, soup) -> dict:
        container = soup.find(id='synopsisDetailsEligibilityTable')
        if container.find('tr') is None:
            container = soup.find(id='forecastDetailsEligibilityTable')
        
        if container is None:
            raise RuntimeError('Container not found')

        entries = container.find_all('tr')
        if len(entries) < 1:
            raise RuntimeError('No entries')

        return self._recordEntries(entries)

    def _getAdditionalInfo(self, soup) -> dict:
        container = soup.find(id='synopsisDetailsAdditionalInfoTable')
        if container.find('tr') is None:
            container = soup.find(id='forecastDetailsAdditionalInfoTable')

        if container is None:
            raise RuntimeError('Container not found')
        
        entries = container.find_all('tr')
        if len(entries) < 1:
            raise RuntimeError('No entries')
        return self._recordEntries(entries)

    def _naviageToRelatedDocuments(self, driver):
        pass





