import sqlite3
from pprint import pprint

class DB:

    connection = sqlite3.connect('test.db')

    #def __init__(self):
        #self.dropTables()
        #self.createTables()

    def getDB(self):
        return self
        
    def getConnection(self) -> sqlite3.Connection:
        return self.connection

    def createTables(self):
        self.connection.execute('''CREATE TABLE CHANNELS
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TITLE TEXT NOT NULL,
        LINK TEXT NOT NULL,
        DESCRIPTION TEXT,
        LAST_BUILD_DATE TEXT NOT NULL,
        LAST_CHECKED TEXT NOT NULL);''')
        
        self.connection.execute('''CREATE TABLE ITEMS
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CHANNEL_ID INT NOT NULL,
        TITLE TEXT NOT NULL,
        LINK TEXT NOT NULL,
        PUB_DATE TEXT NOT NULL,
        DESCRIPTION TEXT NOT NULL,
        CONTENT TEXT NOT NULL,
        AUTHOR TEXT,
        READ BOOLEAN
        );''')

        print('Created Tables')
    
    def dropTables(self):
        self.connection.execute('''
        DROP TABLE IF EXISTS CHANNELS
        ''')

        self.connection.execute('''
        DROP TABLE IF EXISTS ITEMS
        ''')

        print('Dropped Tables')

    def insertFeed(self, fields) -> int:
        cursor = self.connection.cursor()
        cursor.execute('''
        INSERT INTO CHANNELS (TITLE, LINK, LAST_BUILD_DATE, LAST_CHECKED)
        VALUES (?, ?, ?, ?)
        ''', (fields['title'], fields['link'], fields['last_build'], fields['last_checked']))
        self.connection.commit()
        return cursor.lastrowid

    def deleteFeedById(self, id) -> sqlite3.Cursor:
        cursor = self.connection.cursor()
        cursor.execute('''
        DELETE FROM CHANNELS
        WHERE ID = ?
        ''', (id))
        self.connection.commit()
        return cursor

    def getFeeds(self) -> sqlite3.Cursor:
        cursor = self.connection.execute('''
        SELECT * FROM CHANNELS;
        ''')
        return cursor

    def insertItem(self, fields) -> sqlite3.Cursor:
        cursor = self.connection.cursor()
        cursor.execute('''
        INSERT INTO ITEMS (CHANNEL_ID, TITLE, LINK, PUB_DATE, DESCRIPTION, CONTENT, AUTHOR, READ)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (fields['channelId'], fields['title'], fields['link'], fields['pubDate'], fields['description'], fields['content'], fields['author'], False))
        self.connection.commit()
        return cursor

    def getItems(self) -> sqlite3.Cursor:
        cursor = self.connection.execute(
        '''
        SELECT ID, CHANNEL_ID, TITLE, DESCRIPTION, PUB_DATE, READ FROM ITEMS;
        '''
        )
        return cursor

    def getItemById(self, id) -> sqlite3.Cursor:
        cursor = self.connection.execute(
        '''
        SELECT * FROM ITEMS
        WHERE ID = ?
        ''', (id))
        return cursor