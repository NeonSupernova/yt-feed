import timg
import json
import requests
from xmltodict import parse
from rich.console import Console
from PIL import Image
from io import BytesIO

console = Console()

class Cache:
    def __init__(self, channel_list):
        self.channel_list = channel_list
        self.cache_list = None
        
        
    def get(self):
        vidlist = []
        for i in self.channel_list: # iterates channels
            resp = requests.get('https://www.youtube.com/feeds/videos.xml', params={"channel_id": i})
            resp.raise_for_status()
            feed = json.loads(json.dumps(parse(resp.content), indent=4, sort_keys=True))
            for j in feed['feed']['entry']: # iterates videos
                video = Video(j['author']['name'], j['title'], j['published'], j['link']['@href'])
                video.thumbnail(j['media:group']['media:thumbnail']['@url'], j['media:group']['media:thumbnail']['@width'], j['media:group']['media:thumbnail'])
                vidlist.append(video)
        self.cache_list = vidlist
        
                                
    def sort(self, sort_method, list_size, query=None):
        # sort by attribute
        if query != None:
            match sort_method:
                case 'title':
                    filtered_list = [video for video in self.cache_list if video.title == query]
                case 'name':
                    filtered_list = [video for video in self.cache_list if video.name == query]
                case _:
                    raise ValueError('invalid passed')
        else:
            filtered_list = self.cache_list
        filtered_list = sorted(filtered_list, key=lambda video:video.date)
        self.cache_list = filtered_list[-list_size:]

                                
class Video:
    def __init__(self, name, title, date, link):
        self.name = name
        self.title = title
        self.date = date
        self.link = link

    def thumbnail(self, img_link, img_width, img_height):
        self.img_link = img_link
        self.img_width = img_width
        self.img_height = img_height

    def display(self):
        console.print(self.name, style='cyan')
        console.print(self.title, style='blue bold')
        console.print(self.date, style='green italic')
        console.print(self.link)
        print('')

    def img_display(self, method='ascii'):
        if method == 'none':
            return 0
        thumb = requests.get(self.img_link)
        thumb.raise_for_status()
        img = Image.open(BytesIO(thumb.content))
        obj = timg.Renderer()
        obj.load_image(img)
        obj.resize(60, 45)
        if method == 'ascii':
            obj.render(timg.ASCIIMethod)
        elif method == 'ansi':
            obj.render(timg.Ansi24HblockMethod)
