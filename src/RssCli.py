import argparse
import validators
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from feeds.feeds import Feeds
from feeds.items import Items
from pprint import pprint


class RssCli:

    feeds = Feeds()
    items = Items()
    console = Console()

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description='Parse cli args.')
        self.parser.add_argument('-a', '--add', type=str, help='Add RSS feed subscription by url.')
        self.parser.add_argument('-d', '--delete', type=str, help='Remove RSS Feed subscription by id.')
        self.parser.add_argument('-lc', '--listChannels', action="store_true", help="List RSS feed subscriptions.")
        self.parser.add_argument('-li', '--listItems', action="store_true", help="List entries in all feeds.")
        self.parser.add_argument('-id', '--byId', type=str, help="Id modifier to listing feeds and entries.")
        self.parser.add_argument('-r', '--read', type=str, help="Read entry of specified id.")

        self.args = self.parser.parse_args()

    def init(self) -> None:
        args = self.parser.parse_args()
        if (args.add):
            if (validators.url(args.add)):
                self.feeds.add(args.add)
                print('Added RSS feed')
            else:
                print("Please supply a valid url")
        if (args.delete):
            self.feeds.removeFeedById(args.remove)
        if (args.listChannels):
            table = Table(title="RSS Feeds")
            table.add_column("Id")
            table.add_column("Title")
            table.add_column("Last Updated")

            feeds = self.feeds.listFeeds()
            for f in feeds:
                table.add_row(str(f[0]), f[1], f[4])
            self.console.print(table)
        if (args.listItems):
            table = Table(title="Entries")
            table.add_column("Id")
            table.add_column("Channel Id")
            table.add_column("Title")
            table.add_column("Description")
            table.add_column("Published")
            table.add_column("Read")

            items = self.items.getItems()
            for i in items:
                table.add_row(str(i[0]), str(i[1]), i[2], i[3], i[4], str(i[5]))
            self.console.print(table)
        if (args.read):
            item = self.items.getItem(args.read)
            with self.console.pager():
                self.console.print(Markdown(item[6]))

RssCli.init(RssCli())
