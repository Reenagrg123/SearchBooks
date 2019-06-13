import os
from pymongo import MongoClient
import json
import dialogflow_v2 as dialogflow
from pymongo import MongoClient
import re
import dialogflow_v2 as dialogflow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secret.json"
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = 'book-search-bljksb'


client = MongoClient('mongodb+srv://Reena:Reena@cluster0-99md4.mongodb.net/test?retryWrites=true&w=majority')
db = client.get_database('Search_Book')

book_record = db.book_search
novel_record = db.novel_search


def Search_book(parameters):
    title = parameters.get('book_title')
    author=parameters.get('book_author')
   
    if title!="":
        reg = re.compile(title, re.IGNORECASE)
        qry = {"title": {"$regex": reg}}

    elif author!="":
        print('eh')
        reg = re.compile(author, re.IGNORECASE)
        qry = {"authors": {"$regex": reg}}
    
    else:
        resp=[1]
        return resp

    x= book_record.find(qry)
    
    list1=[]
    for i in x:
        list2=[]
        list2.append(i['title'])
        list2.append(i['authors'])
        list2.append(i['infoLink'])
        list2.append(i['thumbnail'])
        list1.append(list2) 
    return list1


def Search_novel(parameters):
    print("hello")
    title = parameters.get('novel_title')
    author=parameters.get('novel_author')
    print(title)
    if title!="":
        reg = re.compile(title, re.IGNORECASE)
        qry = {"title": {"$regex": reg}}

    elif author!="":
        print('eh')
        reg = re.compile(author, re.IGNORECASE)
        qry = {"authors": {"$regex": reg}}
    
    else:
        resp=[1]
        return resp

    rec= novel_record.find(qry)
    print(rec)
    #print(len(list((rec))))
    #print(list(x))
    l1=[]
    for i in rec:
        print("hello")
        l2=[]
        l2.append(i['title'])
        l2.append(i['authors'])
        l2.append(i['infoLink'])
        l2.append(i['thumbnail'])
        l1.append(l2)
        print(l1)
    return l1

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def fetch_reply(message, session_id):
    response = detect_intent_from_text(message, session_id)
    #print(response)
    if response.intent.display_name == 'search_book':
        records = Search_book(dict(response.parameters))
        #records = str(records)
        print(type(records))
        return records

    elif response.intent.display_name == 'search_novel':
        records = Search_novel(dict(response.parameters))
        # records = str(records)
        return records
     
    else:
        return list(response.fulfillment_text)

