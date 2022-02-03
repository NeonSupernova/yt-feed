#!/usr/local/bin/python3.10
import click
from yt_feed import feedutils as fu
import os
import xdg
import json

def create_config():
    # First run creates directory
    if os.path.exists(f"{xdg.XDG_CONFIG_HOME}/yt-feed") != True:
        os.mkdir(f"{xdg.XDG_CONFIG_HOME}/yt-feed")
    # Create conf if not exists
    if os.path.exists(f"{xdg.XDG_CONFIG_HOME}/yt-feed/yt-feed.conf") != True:
        with open(f"{xdg.XDG_CONFIG_HOME}/yt-feed/yt-feed.conf", 'x') as f:
            var = []
            json.dump(var, f)

    # Reading to load conf at start
    # write to conf only with add()





@click.command()
@click.option(
    "--sort", "-s", default='name', help="How to sort the videos.", type=click.Choice(["title", "name"], case_sensitive=False), show_default=True
)
@click.option('--query', '-q', help="String to search for as a channel or title")
@click.option(
    "--output_number",
    "-o",
    type=int,
    default=10,
    help="How many videos are displayed.",
    show_default=True,
)
@click.option(
    "--img",
    "-i",
    default="none",
    help="How to display thumbnails",
    show_default=True,
    type=click.Choice(["none", "ansi", "ascii"], case_sensitive=False),
)
@click.option(
    "--add",
    "-a",
    help="Adds a link to the config"
)
def main(sort, output_number, img, query, add):
    create_config()
    conf = open(f"{xdg.XDG_CONFIG_HOME}/yt-feed/yt-feed.conf", "r")
    if add:
        yt_subs = json.load(conf)
        yt_subs.append(add)
        with open(f"{xdg.XDG_CONFIG_HOME}/yt-feed/yt-feed.conf", "w") as f:
            json.dump(yt_subs, f)
        return
    try:
        cache = fu.Cache(json.load(conf))
    except ConfigError:
        print(ConfigError)
        print("Please add a channel to the list first with --add")
    cache.get()
    cache.sort(sort, output_number, query)
    for i in cache.cache_list:
        i.display()
        i.img_display(img)


if __name__ == "__main__":
    main()


"""
options:
- [x]help menu;
- [x]image display: No img, ascii, ansi;
- [x]amount of things to be displayed;
- [x]sort options: author, date()
- []load subscriptions from
"""
