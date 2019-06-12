import os
from pymongo import MongoClient
import json
import dialogflow_v2 as dialogflow
from pymongo import MongoClient
import re

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()

PROJECT_ID = 'book-search-bljksb'


client = MongoClient('mongodb+srv://Reena:Reena@cluster0-99md4.mongodb.net/test?retryWrites=true&w=majority')
db = client.get_database('Search_Book')

book_record = db.book_search
novel_record = db.Search_Novel  


def Search_book(parameters):
    title = parameters.get('book_title')
    author=parameters.get('book_author')
    print("author:",author)
    #author = parameters.get('book_author')
    if title!="":
        reg = re.compile(title, re.IGNORECASE)
        qry = {"title": {"$regex": reg}}

    elif author!="":
        print('eh')
        reg = re.compile(author, re.IGNORECASE)
        qry = {"authors": {"$regex": reg}}
    
    else:
        return "Please enter any title or author name to search a book"

    x= book_record.find(qry)
    
    # strb='{} books are: '.format(title)+'\n \n'
    list1=[]
    for i in x:
        list2=[]
        list2.append(i['title'])
        list2.append(i['authors'])
        list2.append(i['infoLink'])
        list2.append(i['thumbnail'])
        list1.append(list2)

        # strb += i['title']+" by "+str(i['authors'])+"\n"+ i['infoLink']+"\n\n"
    print(list1)    
    return list1


def Search_novel(parameters):
    title = parameters.get('novel_title')
    reg = re.compile(title, re.IGNORECASE)
    qry = {"title": {"$regex": reg}}
    x= novel_record.find(qry)
    
    strb='{} novels are: '.format(title)+'\n \n'
    
    for i in x:
        strb += i['title']+" by "+str(i['authors'])+"\n"+ i['infoLink']+"\n\n"
    print(strb)    
    return strb



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

    elif response.intent.display_name == 'Search_Novel':
        records = Search_novel(dict(response.parameters))
        # records = str(records)

        return records
     
    else:
        return response.fulfillment_text

