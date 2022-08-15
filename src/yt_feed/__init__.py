#!/usr/local/bin/python3.10

import utils
import os
import json
import argparse
from requests import get

def create_config():
	# Create conf if not exists
	if os.path.exists("./yt-feed.conf") != True:
		with open("./yt-feed.conf", 'x') as f:
			var = []
			json.dump(var, f)

	# Reading to load conf at start
	# write to conf only with add()
def list_config(conf):
	for i in json.load(conf):
		x = parse(get('https://www.youtube.com/feeds/videos.xml', params={"channel_id": i}).content)
		print(x['feed']['entry'][0]['author']['name'])


def parseargs():
	parser = argparse.ArgumentParser(description='Youtube Subs from Terminal')
	parser.add_argument(
		'-s', '--sort',
		default='name', choices=['title', 'name'],
		help='How to sort the videos')
	parser.add_argument(
		'-q', '--query',
		help='query')
	parser.add_argument(
		'-o', '--output_number',
		default=10, type=int,
		help="String to search for as a channel or title")

	parser.add_argument(
		'-a', '--add',
		help='Adds a channel id to the config')

	parser.add_argument(
		'-l', '--list',
		action="store_true",
		default="False",
		help='list channels in config')

	args = parser.parse_args()
	return args


def main():
	create_config()
	args = vars(parseargs())
	conf = open("./yt-feed.conf", "r")
	if args['list'] == True:
		list_config(conf)
		return
	if args['add'] != None:
		yt_subs = json.load(conf)
		yt_subs.append(args['add'])
		with open("./yt-feed.conf", "w") as f:
			json.dump(yt_subs, f)
	feed = utils.Feed(json.load(conf))
	feed.sort(
		args['sort'],
		args['output_number'],
		args['query'])
	for i in feed.feed:
		i.display()


if __name__ == "__main__":
	main()
