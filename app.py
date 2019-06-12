from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from utils import fetch_reply

app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def sms_reply():
    message = request.form.get('Body')
    sender = request.form.get('From')

    response = MessagingResponse()

    records=fetch_reply(message, sender)
   
    for rec in records:
        x=""
        y=""
        x+="\nTitle: "+rec[0]+"\nAuthors: "+str(rec[1])+"\n "+"\nInfo Link:"+"\n"+rec[2]
        y+=rec[3]
        response.message('{}'.format(x)).media(y)  
    return str(response)
 


    # print(type(x))
    # print(x[1])

    # response.message('x[0][0]')

    
if __name__ == '__main__':
    app.run(debug=True)

