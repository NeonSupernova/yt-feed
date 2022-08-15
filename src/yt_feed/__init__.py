#!/usr/local/bin/python3.10

from .utils import Feed
import os
import json
import argparse
from xmltodict import parse
from requests import get

DEFAULT_CONFIG = f"{os.getenv('HOME')}.config/yt-feed.conf"


def list_config(conf):
    with open(conf, "r") as f:
        for i in json.load(f):
            x = parse(
                get(
                    "https://www.youtube.com/feeds/videos.xml", params={"channel_id": i}
                ).content
            )
            print(x["feed"]["entry"][0]["author"]["name"])


def add_config(conf, sub):
    with open(conf, "r") as f:
        content = json.load(f)
        content.append(sub)
        with open(conf, "w") as f:
            json.dump(content, f)


def rm_config(conf, sub):
    with open(conf, "r") as f:
        content = json.load(f)
        content.pop(sub)
        with open(conf, "w") as f:
            json.dump(content, f)


def parseargs():
    parser = argparse.ArgumentParser(description="Youtube Subs from Terminal")
    parser.add_argument(
        "-s",
        "--sort",
        default="name",
        choices=["title", "name"],
        help="How to sort the videos",
    )
    parser.add_argument("-q", "--query", help="query")
    parser.add_argument(
        "-o",
        "--output_number",
        default=10,
        type=int,
        help="String to search for as a channel or title",
    )
    parser.add_argument("-a", "--add", help="Adds a channel id to the config")
    parser.add_argument("-rm", "--remove", help="Removes a channel id from the config")
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        default="False",
        help="list channels in config",
    )
    parser.add_argument(
        "-c", "--config", default=DEFAULT_CONFIG, help="Sets config to use"
    )
    args = parser.parse_args()
    return args


def main():
    args = vars(parseargs())
    if args["list"] == True:
        list_config(conf)
        return
    if args["add"] != None:
        add_config(conf, args["add"])
        return
    if args["remove"] != None:
        rm_config(conf, args["rm"])
        return
    feed = Feed(json.load(conf))
    feed.sort(args["sort"], args["output_number"], args["query"])
    for i in feed.feed:
        i.display()


if __name__ == "__main__":
    main()
