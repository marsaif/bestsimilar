from time import sleep
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Scraper :

    def __init__(self) -> None:
        self.counter = 2

        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
        self.driver.maximize_window()

    def get_movie_info(self) -> List[dict]:
        info = {
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

        div_content = self.driver.find_element(By.CLASS_NAME,"column-content-c")
        attrs = div_content.find_elements(By.CLASS_NAME,"attr")
        for attr in attrs:
            type = attr.find_element(By.CLASS_NAME,"entry").text[:-1]
            data = attr.find_element(By.CLASS_NAME,"value").text
            info[type] = data

        img = self.driver.find_element(By.CLASS_NAME,"img-responsive")
        info['image_url'] = img.get_attribute("src")
        print(info)


    def get_movies(self) -> None :
        url = f"https://bestsimilar.com/movies/{self.counter}"
        self.driver.get(url)
        self.get_movie_info()
    
    