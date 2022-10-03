from db.db import DB
from markdownify import markdownify as md
from pprint import pprint

class Items:
    db = DB()

    def insertItem(self, fields, channelId):
        insert = {
            'channelId': channelId,
            'title': fields['title'],
            'link': fields['link'],
            'pubDate': fields['published'],
            'description': fields['summary'],
            'content': md(fields['content'][0]['value']),
            'author': fields['author'],
            'read': False
        }
        self.db.insertItem(insert)

    def getItems(self):
        items = self.db.getItems()
        return items.fetchall()

    def getItem(self, id):
        item = self.db.getItemById(id).fetchall()
        return item[0]
