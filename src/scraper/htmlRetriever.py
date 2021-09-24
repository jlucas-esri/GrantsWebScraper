import requests

class HtmlRetriever:

    def __init__(self, link):
        self.link = link
        self.response = requests.get(link)
        self.response.raise_for_status()
        self.content = self.response.content

    @staticmethod
    def main(link):
        retriever = HtmlRetriever(link)
        return retriever.content
        
        