import json
from typing import List
from bs4 import BeautifulSoup
import requests
import translators as ts

class Scraper :

    def __init__(self) -> None:
        self.counter = 1

    def get_movie_info(self,soup : BeautifulSoup) -> dict:
        info = {
            'trailer' : '' , 
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
            'image_url' : '' ,
            'image_name' : '',
            'Audience' : ''
            }
        div_content = soup.select_one(".item-c")

        title = div_content.select_one(".name-c").find("span").getText()
        info['title'] = title

        image_name = title.replace(" ","-")
        info['image_name'] = image_name.replace(")","").replace("(","")
        trailer = div_content.select_one(".watch-c")
        if trailer:
            trailer = trailer.find("button")['data-video']
        else:
            trailer = ''

        info['trailer'] = f"https://www.youtube.com/watch?v={trailer}"

        attrs = div_content.select(".attr")
        for attr in attrs:
            type = attr.select_one(".entry").getText()[:-1]
            data = attr.select_one(".value").getText().strip()
            info[type] = data

        img = div_content.select_one(".img-responsive")
        info['image_url'] = img['src']
        info['Duration'] = info['Duration'].replace("min.","").strip()
        return info

    def translate_movies_info(self,info : dict) : 
        info['Time'] = "20th century, victorian era, 19th century, post world war one, 20th century, post world war two, future, 22nd century, 23rd century, distant future"
        
        info['Story'] = ts.google(info['Story'], from_language='en', to_language='nl')
        info['Country'] = ts.google(info['Country'], from_language='en', to_language='nl')
        info['Style'] = ts.google(info['Style'], from_language='en', to_language='nl')
        info['Genre'] = ts.google(info['Genre'], from_language='en', to_language='nl')
        info['Place'] = ts.google(info['Place'], from_language='en', to_language='nl')
        info['Time'] = ts.google(info['Time'], from_language='en', to_language='nl')
        info['Plot'] = ts.google(info['Plot'], from_language='en', to_language='nl')
        info['Audience'] = ts.google(info['Audience'], from_language='en', to_language='nl')

        return info

    def is_movie(self,soup : BeautifulSoup) :
        div_content = soup.select_one(".item-c")
        tv_show = div_content.select_one(".attr-types")
        return tv_show == None
            

    def get_movies(self) -> None :

        while True:
            url = f"https://bestsimilar.com/movies/{self.counter}"
            headers = {'User-Agent': ''}

            response = requests.get(url,headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            h1 = soup.find("h1").getText()
            if h1 == "Page not found" :
                break

            if self.is_movie(soup) : 
                info = self.get_movie_info(soup)
                #print(json.dumps(info, indent=2, default=str))
                translated_info = self.translate_movies_info(info)
                print(json.dumps(translated_info, indent=2, default=str))
            
            self.counter = self.counter + 1 


