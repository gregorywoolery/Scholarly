import os, sys
import json
from flask import Flask, request
import requests
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAD78R15hcQBAFTr5Q3tgDOSOIJWseOPSErIdrBS8lqAQwa9agTaJjiztIRv0yl6pr0O5eLh4oZBNY8UoeRZAz7Gim0hybZAbTZBdguwpwzj9olZBsDrPj3rZBjbEVVC7sPR9Md3Ie6mNpr1RWjKYS5m1OIu7OtloNQCOedfoIijcUafkpfgPw"
bot = Bot(PAGE_ACCESS_TOKEN)

VERIFICATION_TOKEN = "Sl33pyW00ly"

GREETINGS = ['Is anyone available to chat?', 'Hey', 'hey', 'Hi', 'hi', 'hello', 'good afternoon', 'i have a question']


buttons = [
    {
        'YEARS':["Year 1", "Year 2", "Year 3", "Final Year"],
        'payload': 1
    },
    {
        'MAJORS':["Computer Science", "Social Sciences", "Medicine", "Pharmacy" "Any"],
        'payload': 2
    }

]


@app.route('/', methods=['GET'])
def verify():
    #Webhook Verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "WEBHOOK VERIFIED", 200
    getstarted()

def getstarted():
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"get_started": {"payload": "GET_STARTED_PAYLOAD"}})
    r = requests.post('https://graph.facebook.com/v7.0/me/messenger_profile?access_token='+ PAGE_ACCESS_TOKEN, headers=headers, data=data)

@app.route('/', methods=['POST'])
def webhook():
    print(request.data)
    data = request.get_json()

    if data['object'] == "page":
        entries = data['entry']

        for entry in entries:
	        messaging = entry['messaging']
			
        for messaging_event in messaging:
            sender_psid = messaging_event['sender']['id']
            recipient_psid = messaging_event['recipient']['id']

        #Handles messages events
        if messaging_event.get('message'):
            handleMessage(sender_psid, messaging_event['message'])
                    
        elif messaging_event.get('postback'):
            handlePostback(sender_psid, messaging_event['postback'])

        return "ok", 200
    else:
        #Return a '404 Not Found' if event is not from a page subscription
        return "error", 404

#handles message reply
def handleMessage(sender_psid, received_message):
    response = {}

    if ('quick_reply' in received_message.keys()):
            payload = received_message['quick_reply']['payload']
            response_message = received_message['text']
            if payload == buttons[0]['payload']:
                years = received_message
                response = {
                    "attachment": {
                        "type":"template",
                        "payload": {
                            "template_type":"generic",
                            "elements":[
                                {
                                    "title":"University of Technology",
                                    "image_url":"https://www.utech.edu.jm/about-utech/utech.jpg",
                                    "subtitle":"UTech",
                                    "default_action": {
                                        "type": "postback",
                                        "payload": "matchUtech",
                                        "messenger_extensions": False,
                                        "webview_height_ratio": "COMPACT"
                                    },
                                    "buttons":[
                                        {
                                            "type":"web_url",
                                            "url":"https://www.marriott.com/hotels/travel/sdqds-sheraton-santo-domingo-hotel/?scid=bb1a189a-fec3-4d19-a255-54ba596febe2&y_source=1_Mjg2ODk3OC03MTUtbG9jYXRpb24uZ29vZ2xlX3dlYnNpdGVfb3ZlcnJpZGU=",
                                            "title":"Full Listing"
                                        },
                                        {
                                            "type": "postback",
                                            "title": "Find your match",
                                            "payload": "matchUtech"
                                        }
                                    ]      
                                },
                                {
                                    "title":"University of the West Indies",
                                    "image_url":"https://sta.uwi.edu/newspics/2020/Regional%20crest%20INtranet.jpg",
                                    "subtitle":"UWI",
                                    "default_action": {
                                        "type": "postback",
                                        "payload": "matchUWI",
                                        "messenger_extensions": False,
                                        "webview_height_ratio": "COMPACT"
                                    },
                                    "buttons":[
                                        {
                                            "type":"web_url",
                                            "url":"https://www.mona.uwi.edu/osf/scholarships-bursaries",
                                            "title":"Full Listing"
                                        },
                                        {
                                            "type": "postback",
                                            "title": "Find your match",
                                            "payload": "matchUWI"
                                        }
                                    ]     
                                },
                                {
                                    "title":"Other",
                                    "image_url":"https://s3-ap-southeast-2.amazonaws.com/geg-web/public/images/300x200/1596434755-unimelb.png",
                                    "subtitle":"Jamaica",
                                    "default_action": {
                                        "type": "postback",
                                        "payload": "matchAny",
                                        "messenger_extensions": False,
                                        "webview_height_ratio": "COMPACT"
                                    },
                                    "buttons":[
                                        {
                                            "type": "postback",
                                            "title": "Find your match",
                                            "payload": "matchAny"
                                        }
                                    ]       
                                }
                            ],
                        }
                    }
                }

    if 'text' in received_message:
        messaging_text = received_message['text']
        if messaging_text in GREETINGS:
            firstName = getFirstName(sender_psid)
            response = "Welcome to Scholarly" + firstName +". Where the scholarships island wide are placed in a easy to access way for all university students."
            response2 = "Please Select your year."  
            bot.send_text_message(sender_psid, response2)
            postback_button_response(response2, , YEARS)
            response = {
                "text": response2
            }
            callSendAPI(sender_psid, response2)
        if messaging_text in YEARS:
            year = messaging_text 
            response = "Excellect !"
            bot.send_text_message(sender_psid, response)
            response = "Major ?."
            callSendAPI_QuickReplyDegree(sender_psid, response, )
        if messaging_text in MAJORS:
            major = messaging_text
            response = "That's amazing ! 1's and 0's are the way of life !"
            bot.send_text_message(sender_psid, response)
            response2 = "Institution ?"
            callSendAPI_QuickReplySch(sender_psid, response2)
        if 'UTECH' in messaging_text:
            response = "Thank you.. Please give us a sec"
            callSendAPI_TextMessage(sender_psid, response)
            response = "Computing results..."
            callSendAPI_TextMessage(sender_psid, response)

def postback_button_response(text, payload, titles):
    quick_replies = []
    for title in titles:
        quick_replies.append({
            'content_type': 'text',
            'title': title,
            'payload' : payload,
        })

    return {
        'text': text,
        'quick_replies': quick_replies
    }

# Sends response messages via the Send API
def callSendAPI(sender_psid, response):
    headers = {"Content-Type": "application/json"}
    data = json.dumps(
        {"recipient": {
            "id": sender_psid
            },
            "message": response,
            "sender_action": None
        })

    try:
        r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)
        print (r.text)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        pass
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        pass
    else:
        print('Success!')

# Sends response quick reply messages via the Send API
def callSendAPI_QuickReply(sender_psid, response, ):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "recipient": {
            "id": sender_psid
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": response,
            "quick_replies":[
            {
                    "content_type":"text",
                    "title":"Year 1",
                    "payload":"year1",
                },
                {
                    "content_type":"text",
                    "title":"Year 2",
                    "payload":"year2",                      
                },
                {
                    "content_type":"text",
                    "title":"Year 3",
                    "payload":"year3",
                },
                {
                    "content_type":"text",
                    "title":"Final Year",
                    "payload":"final",
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


def handlePostback(sender_psid, received_postback):
    test = "thanks for being here"


@app.route('/', methods=['GET'])
def getFirstName(sender_id):
    
    params = {
        ("fields", "first_name"),
        ("access_token", PAGE_ACCESS_TOKEN)
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.get("https://graph.facebook.com/"+sender_id, params=params, headers=headers)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)
    return r.text


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug = True, port = 80)