import time
import logging
from selenium.common.exceptions import NoSuchElementException

class IteratePages:

    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

    def __init__(self, driver):
        self.driver = driver
        self.driver.switch_to.default_content()
        self.driver.switch_to_frame('embeddedIframe')
    
    # @staticmethod
    # def run():
    #     pass
    
    def __iter__(self):
        self.iteratedOnce = False
        return self

    def __next__(self):
        try:
            if not self.iteratedOnce:
                self.iteratedOnce = True
                return self.driver
            nextButton = self.driver.find_element_by_css_selector('a[title=\"Click Next Page\"]')
            nextButton.click()
            #leaving time for the page to load
            time.sleep(3)

            self.driver.switch_to.default_content()
            self.driver.switch_to_frame('embeddedIframe')
            return self.driver
        except NoSuchElementException as e:
            self._logger.debug('No more pages left')
            raise StopIteration

    
    def _iterate(self):
        pass


