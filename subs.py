#!/usr/local/bin/python3.10
import click
import subutils


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
def main(sort, output_number, img, query):
    yt_chan = [
        "UC4qdHN4zHhd4VvNy3zNgXPA",
        "UC6XAct-Bus4x3mYz3VC_HUw",
        "UCwqJYTxm3FAZXeV58EdFcRQ",
        "UCxucf8O8itcmkqu3d7yUavg",
        "UCFqmcAvY-lLQHJcfOHJavGQ",
        "UCeBnbqt4VRhotq2TQjkIi2A",
        "UChd1FPXykD4pust3ljzq6hQ",
        "UCS5Oz6CHmeoF7vSad0qqXfw",
        "UCzTlXb7ivVzuFlugVCv3Kvg",
    ]
    cache = subutils.Cache(yt_chan)
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
