import requests
import json

import requests
from pymongo import MongoClient


class Api:
    
    __BASEURL = 'https://www.googleapis.com/books/v1'
    def __init__(self ):
       pass 

    def _get(self, path, params=None):
        if params is None:
            params = {}
        resp = requests.get(self.__BASEURL+path, params=params)
        if resp.status_code == 200:
            return json.loads(resp.content)

        return resp

    def get(self, volumeId, **kwargs):
      
        path = '/volumes/'+volumeId
        params = dict()
        for p in 'partner projection source'.split():
            if p in kwargs:
                params[p] = kwargs[p]

        return self._get(path)
    
    def list(self, q, **kwargs):
       
        path = '/volumes'
        params = dict(q=q)
        for p in 'download filter langRestrict libraryRestrict maxResults orderBy partner printType projection showPreorders source startIndex'.split():
            if p in kwargs:
                params[p] = kwargs[p]

        return self._get(path, params)


client = MongoClient('mongodb+srv://Reena:Reena@cluster0-99md4.mongodb.net/test?retryWrites=true&w=majority')
db = client.get_database('Search_Book')
book_record = db.Search_Book  
novel_record = db.Search_Novel      


def get_book_data():
        api=Api()
        list_books=['python','C#','java','Flask','C']
        list_novels=['A Fine Balance',"Midnight's Children",'The Glass Palace','The Interpreter Of Maladies','The Story Of My Experiments With The Truth']

        for i in range(0,5):
            book_dict={}
            novel_dict={}
            book_dict=api.list('list_books[i]')
            novel_dict=api.list('list_novels[i]')
        #return data_dict
            #print(book_dict)
            print(len(book_dict['items']))
            for i in range(0,len(book_dict['items'])):
                
                record_dict={}
                record_dict['title']=book_dict['items'][i]['volumeInfo']['title']
                record_dict['authors']=book_dict['items'][i]['volumeInfo']['authors']
                record_dict['infoLink']=book_dict['items'][i]['volumeInfo']['infoLink']
                print(record_dict)

                book_record.insert_one(record_dict)
            print("hello")
          
get_book_data()