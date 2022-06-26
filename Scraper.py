import json
from time import sleep
from typing import List
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Scraper :

    def __init__(self) -> None:
        self.counter = 1

        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
        #self.driver.maximize_window()

    def get_movie_info(self,soup : BeautifulSoup) -> List[dict]:
        info = {
            'title' : '',
            'Original name' : '' , 
            'Genre' : '' , 
            'Country' : '' , 
            'Duration' : '' , 
            'Story' : '' , 
            'Style' : '' , 
            'Plot' : '' ,
            'Time' : '', 
            'Place' : '' , 
            'image_url' : ''
            }

        div_content = soup.select_one(".column-content-c")
        attrs = div_content.select(".attr")
        for attr in attrs:
            type = attr.select_one(".entry").getText()[:-1]
            data = attr.select_one(".value").getText().strip()
            info[type] = data

        img = soup.select_one(".img-responsive")
        info['image_url'] = img['src']
        print(json.dumps(info, indent=2, default=str))


    def get_movies(self) -> None :
        url = f"https://bestsimilar.com/movies/{self.counter}"
        headers = {'User-Agent': ''}

        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        self.get_movie_info(soup)
    
    