import requests
import feedparser
import datetime
from db.db import DB
from feeds.items import Items
from pprint import pprint
from inspect import _void
from tokenize import String

class Feeds:
    db = DB()
    items = Items()

    def __fetch(url) -> String:
        response = ''
        try:
            response = requests.get(url)
        except requests.ConnectionError as e:
            print('Unable to connect to supplied url. Is it correct?')
        except requests.exceptions.Timeout as e:
            print('Timeout error. Is the internet unplugged?')
        except requests.exceptions.TooManyRedirects as e:
            print('Too many redirects, is the url correct?')
        except requests.exceptions.RequestException as e:
            print('Bad request, is the url correct?')
        finally:
            if (response):
                return(response.text)
            else:
                print('Problem with response. Feed not added')
                return ''
    
    def add(self, url):
        text = Feeds.__fetch(url)
        feed = feedparser.parse(text)
        fields = {
            'title': feed.feed.title,
            'link': feed.feed.link,
            'last_build': feed.feed.updated,
            'last_checked': datetime.datetime.now().isoformat()
        }
        channelId = self.db.insertFeed(fields)
        for entry in feed.entries:
            self.items.insertItem(entry, channelId)

    def listFeeds(self):
        return self.db.getFeeds().fetchall()

    def removeFeedById(self, id):
        return self.db.deleteFeedById(id)
        
    # Parse RSS feed into fields.
    #def __parse(text):


