import requests

class HtmlRetriever:

    def __init__(self, driver):
        self.content = driver.page_source

    @staticmethod
    def main(driver):
        retriever = HtmlRetriever(driver)
        return retriever.content
        
        