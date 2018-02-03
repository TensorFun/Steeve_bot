# from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .model_cmd import *
from .messenger_api import *
from .credentials import VERIFY_TOKEN

# Create your views here.

def post_facebook_message(fbid, recevied_message):
    # user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    # user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}
    # user_details = requests.get(user_details_url, user_details_params).json()

    fb = FbMessageApi(fbid)

    if recevied_message == "Google":
        fb.image_message("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/1200px-Google_2015_logo.svg.png")
        return 0
    if recevied_message == "Facebook":
        fb.image_message("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Facebook_New_Logo_%282015%29.svg/2000px-Facebook_New_Logo_%282015%29.svg.png")
        return 0
    if recevied_message == "Company":
        data = [
            {
                "content_type": "text",
                "title": "Google",
                "payload": "Google"
            },
            {
                "content_type": "text",
                "title": "Facebook",
                "payload": "Facebook"
            }
        ]
        fb.quick_reply_message(
            text="你想看哪家公司的logo?",
            quick_replies=data)
        return 0 
    if recevied_message == "Frontend":
        content = steeve_crawler("Frontend")
        fb.text_message(content)
        return 0
    if recevied_message == "Backend":
        content = steeve_crawler("Backend")
        fb.text_message(content)
        return 0
    if recevied_message == "Personal":
        data = [
            {
                "content_type": "text",
                "title": "Frontend",
                "payload": "Frontend"
            },
            {
                "content_type": "text",
                "title": "Backend",
                "payload": "Backend"
            }
        ]
        fb.quick_reply_message(
            text="我可以隨機推薦一個工作給你，你想要什麼領域?",
            quick_replies=data)
        return 0    
    if recevied_message == "Hello TensorFun":
        data = [
            {
                "content_type": "text",
                "title": "Personal",
                "payload": "Personal"
            },
            {
                "content_type": "text",
                "title": "Company",
                "payload": "Company"
            }
        ]
        fb.quick_reply_message(
            text="You are?",
            quick_replies=data)
        return 0
    data = [
        {
            "type": "postback",
            "title": "Hello TensorFun",
            "payload": "Hello TensorFun"
        },
        {
            "type": "web_url",
            "url": "https://www.atositchallenge.net/",
            "title": "Atos IT Challenge 2018"
        }, {
            "type": "web_url",
            "url": "http://www.nlplab.cc/",
            "title": "NLP LAB, NTHU"
        }
    ]    
    fb.template_message(
        title="May I help you?",
        image_url="https://i.imgur.com/7vVkVkd.png",
        subtitle="Steeve",
        data=data)
    return 0  


class MyBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    # pprint(message)
                    print('message')
                    try:
                        post_facebook_message(message['sender']['id'], message['message']['text'])
                    except:
                        return HttpResponse()
                if 'postback' in message:
                    # pprint(message)
                    print('postback')
                    try:
                        post_facebook_message(message['sender']['id'], message['postback']['payload'])
                    except:
                        return HttpResponse()

        return HttpResponse()
