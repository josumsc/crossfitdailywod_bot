import requests
from bs4 import BeautifulSoup

url = "https://www.crossfit.com/workout"

class WODCrawler:
    def __init__(self, url: str=url):
        self.url = url
        self.wods = {}

    def download_crossfit_wods(self) -> dict:
        """Crawls the CrossFit website and extracts the WODs for each day.

        :return: A dictionary of WODs, where the keys are the dates and the values are the WOD details.
        :rtype: dict
        """
        if self.wods:
            return self.wods

        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")

        content_containers = soup.find_all("div", class_="content-container")
        for container in content_containers:
            date = container.find("h3").text.strip().split()[-1]
            wod_details = container.find("div", class_="col-sm-6").text.strip()
            self.wods[date] = wod_details

        return self.wods
    