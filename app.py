import os, sys
import json
from flask import Flask, request
import requests
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAD78R15hcQBAFTr5Q3tgDOSOIJWseOPSErIdrBS8lqAQwa9agTaJjiztIRv0yl6pr0O5eLh4oZBNY8UoeRZAz7Gim0hybZAbTZBdguwpwzj9olZBsDrPj3rZBjbEVVC7sPR9Md3Ie6mNpr1RWjKYS5m1OIu7OtloNQCOedfoIijcUafkpfgPw"
bot = Bot(PAGE_ACCESS_TOKEN)

VERIFICATION_TOKEN = "Sl33pyW00ly"

GREETINGS = ['Is anyone available to chat?', 'Hey', 'hey', 'Hi', 'hi', 'hello', 'Hello', 'good afternoon', 'i have a question']

buttons = [
    {
        'response': ['Yes', 'No'],
        'payload': '0'
    },    
    {
        'YEARS':["1st Year", "2nd Year", "3rd Year", "Final Year"],
        'payload': '1'
    },
    {
        'MAJORS':["Computer Science", "Social Sciences", "Medicine", "Any"],
        'payload': '2'
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
    data = json.dumps({
        "get_started": {
            "payload": "GET_STARTED_PAYLOAD"
            }
    })

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
        if (payload == buttons[1]['payload']):
            years = received_message
            response = {
                "text": "That's great. We have a few listings here.."
            }
            callSendAPI(sender_psid, response)
            response = {
                "attachment": {
                    "type":"template",
                    "payload": {
                        "template_type":"generic",
                        "elements":[
                            {
                                "title":"University of Technology",
                                "image_url":"https://www.utech.edu.jm/about-utech/utech.jpg",
                                "subtitle":"Utech",
                                "buttons":[
                                    {
                                        "type":"web_url",
                                        "url":"https://www.utech.edu.jm/admissions/dsf/financial-aid/scholarships/scholarships-listing",
                                        "title":"Full Listing",
                                        "webview_height_ratio": "full",
                                        "messenger_extensions": "true",  
                                        "fallback_url": "https://www.utech.edu.jm/admissions/dsf/financial-aid/scholarships/scholarships-listing"
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Scholarship Form",
                                        "payload":"3"
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Find your match",
                                        "payload":"4"
                                    }              
                                ]      
                            },
                            {
                                "title":"University of the West Indies",
                                "image_url":"https://sta.uwi.edu/newspics/2020/Regional%20crest%20INtranet.jpg",
                                "subtitle":"UWI",
                                "buttons":[
                                    {
                                        "type":"web_url",
                                        "url":"https://www.mona.uwi.edu/osf/scholarships-bursaries",
                                        "title":"Full Listing",
                                        "webview_height_ratio": "full",
                                        "messenger_extensions": "true",  
                                        "fallback_url": "https://www.mona.uwi.edu/osf/scholarships-bursaries"
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Scholarship Form",
                                        "payload":"5"
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Find your match",
                                        "payload":"6"
                                    }              
                                ]      
                            },
                            {
                                "title":"Other",
                                "image_url":"https://s3-ap-southeast-2.amazonaws.com/geg-web/public/images/300x200/1596434755-unimelb.png",
                                "subtitle":"Jamaica",
                                "buttons":[
                                    {
                                        "type":"postback",
                                        "title":"Find your match",
                                        "payload":"6"
                                    }              
                                ]      
                            }                            
                        ]
                    }
                }
            }

        elif (payload == buttons[0]['payload']):
            specialNeeds = received_message['text']
            response = {
                "text": "Let's get this show on the road!"
            }
            callSendAPI(sender_psid, response)
            response = "What year are you in ?" 
            response = postback_button_response(response, buttons[1]['payload'], buttons[1]['YEARS'])

        callSendAPI(sender_psid, response)
        return

    elif('attachment' in received_message.keys()):
        atPayload = received_message['attachment']['payload']
        if('generic' in atPayload['template_type']):
            if 'postback' in atPayload['elements']['buttons']['type']:
                payload = atPayload['elements']['buttons']['payload']
                response = "Can we get some information about your Major ?"
                response = postback_button_response(response, buttons[2]['payload'], buttons[2]['MAJORS'])
                callSendAPI(sender_psid, response)
                

    elif 'text' in received_message.keys():
        messaging_text = received_message['text']
        if messaging_text in GREETINGS:
            try:
                firstName = retrieve_user_information(sender_psid)['first_name']
            except:
                firstName = ''
            response = "Hey " + firstName + ", I'm Scholly your assistant bot for today."
            response = {
                "text": response
            }
            callSendAPI(sender_psid, response)
            response = "Welcome to Scholarly, where the scholarships island wide are placed in a easy to access way for all university students." 
            response = {
                "text": response
            }
            callSendAPI(sender_psid, response)
            response = {
                "text": "First we will need to know a little about you."
            }
            callSendAPI(sender_psid, response)
            response = "Are you a special needs student ?"
            response = postback_button_response(response, buttons[0]['payload'], buttons[0]['response'])
            callSendAPI(sender_psid, response)


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


def handlePostback(sender_psid, received_postback):
    if("postback" in received_postback):
        payload = received_postback["postback"]
        if (payload == '3'):
            response = {
                "text": "https://www.surveymonkey.com/r/UTECHScholarshipApplication"
            }
            callSendAPI(sender_psid, response)

        if (payload == '5'):
            response = {
                "text": "https://www.mona.uwi.edu/osf/sites/default/files/osf/scholarship_bursary_application_form_2020_2021.pdf"
            }
            callSendAPI(sender_psid, response)


def retrieve_user_information(sender_psid):
    try:
        # Send the HTTP request to the Messenger Platform
        response = requests.get("https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}".format(sender_psid, PAGE_ACCESS_TOKEN))

        # If the response was successful, no Exception will be raised
        #response.raise_for_status()

        return json.loads(response.content)
    except requests.HTTPError as http_err:
        pass
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        pass
    else:
        print('Success!')

def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug = True, port = 80)