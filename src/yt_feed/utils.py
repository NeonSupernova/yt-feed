import aiohttp
import rich
from xmltodict import parse
import asyncio
import json

class Feed:
	def __init__(self, var: list, loop = None):
		self.list = var
		if loop != None and loop.is_closed() != True:
			self.loop = loop
		else:
			self.loop = asyncio.new_event_loop()
		try:
			self.data = self.loop.run_until_complete(asyncio.wait([self.fetch(i) for i in self.list], timeout=1))
		except KeyboardInterrupt:
			pass
		finally:
			self.loop.close()
		self.feed = []
		for i in self.data[0]:
			for j in i.result()['feed']['entry']:
				self.feed.append(Video(j))
		
	def sort(self, sort_method, list_size, query=None):
		if query != None:
			if sort_method == 'title':
				filtered_list = [
					video for video in self.feed
					if query.casefold() in video.title.casefold()
					]
			elif sort_method == 'name':
				filtered_list = [
					video for video in self.feed if video.author['name']== query
					]
			else:
				raise ValueError('invalid sort method passed')
		else:
			filtered_list = self.feed
		filtered_list = sorted(filtered_list, key=lambda video: video.published)
		self.feed = filtered_list[-list_size:]
		
	async def fetch(self, channel):
		async with aiohttp.ClientSession() as session:
			async with session.get(
			'https://www.youtube.com/feeds/videos.xml',
			params = {"channel_id": channel}
			) as response:
				jsonobject = await response.text()
		return parse(jsonobject)

class Video:
	def __init__(self, js):
		self.author = js['author']
		self.id = js['id']
		self.link = js['link']['@href']
		self.media = js['media:group']
		self.thumbnail = js['media:group']['media:thumbnail']['@url']
		self.published = js['published']
		self.title = js['title']
		self.updated = js['updated']
		self.channelId = js['yt:channelId']
		self.videoId = js['yt:videoId']
		

	def display(self):
		rich.print(f"[magenta bold]{self.author['name']}[/magenta bold]")
		rich.print(f'[blue bold]{self.title}[/blue bold]')
		rich.print(f'[green]{self.published}[/green]')
		rich.print(f"{self.link}")
		print('')
