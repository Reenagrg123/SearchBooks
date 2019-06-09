import os
from pymongo import MongoClient
import json
import dialogflow_v2 as dialogflow
from pymongo import MongoClient

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()

PROJECT_ID = 'book-search-bljksb'


client = MongoClient('mongodb+srv://Reena:Reena@cluster0-99md4.mongodb.net/test?retryWrites=true&w=majority')
db = client.get_database('Search_Book')
book_record = db.Search_Book  
novel_record = db.Search_Novel  


def Search_book(parameters):
    topic = parameters.get('topic')
    record = book_record.find({'category': topic})
    return record

def Search_novel(parameters):
    topic = parameters.get('topic')
    record = book_record.find({'category': topic})
    return record

# def ShowArtistEvents(parameters):
#     #event = parameters.get('entertainment_type')
#     artist = parameters.get('music-artist')
#     record = event_record.find({'artist': artist}).limit(3)
#     return record


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def fetch_reply(message, session_id):
    response = detect_intent_from_text(message, session_id)
    if response.intent.display_name == 'Search_Book':
        records = Search_book(dict(response.parameters))
        records = str(records)

    else if response.intent.display_name == 'Search_Novel'::
        records = Search_novel(dict(response.parameters))
        records = str(records)

    return(records)
     
    else:
        return response.fulfillment_text

