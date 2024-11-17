#!/usr/bin/env python
# coding: utf-8

# # [Line Dev](https://developers.line.biz/zh-hant/)

# In[1]:


import os
import random
import pickle
import pandas as pd
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    CarouselTemplate,
    CarouselColumn,
    MessageAction,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)


# In[2]:


def Load_Pickle(Filename):
    with open(Filename, 'rb') as handle:
        return pickle.load(handle)


# In[3]:


def Create_Template_Message(Group, Figure_list):
    
    temp_sub_group = Group.groupby(['圖片', '選單'])
    temp_columns_list = []
    for key in temp_sub_group.groups:
        this_fig_name = [x for x in Figure_list if x.startswith(key[0])][0]
        this_url = request.url_root + f'static/{this_fig_name}'
        this_url = this_url.replace("http", "https")
        this_title_name = key[1]
        this_group = temp_sub_group.get_group(key)
        # print(this_url, this_title_name)
    
        temp_actions_list = []
        for sub_key in this_group.values:
            this_label = sub_key[4]
            this_text = sub_key[5]
            temp_actions_list.append(MessageAction(label=this_label, text=this_text))
        # print(temp_actions_list)
    
        temp_columns_list.append(
            CarouselColumn(
                thumbnail_image_url=this_url,
                title=this_title_name,
                text='想了解哪個？',
                actions=temp_actions_list
            )
        )
    
    return CarouselTemplate(columns=temp_columns_list)


# In[5]:


fig_list = os.listdir('./static/')
QA_dict = Load_Pickle('./data/QA_dict.pickle')
Keywords_QA_dict = Load_Pickle('./data/Keywords_QA_dict.pickle')
keywords_df = Load_Pickle('./data/keywords_df.pickle')
infos_carousel_df = Load_Pickle('./data/infos_carousel_df.pickle')
infos_carousel_groups = infos_carousel_df.groupby('圖文')


# In[7]:


app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(channel_secret=os.getenv('LINE_CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    event_status = False
    event_token = event.reply_token
    event_message = event.message.text
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if event_message in Keywords_QA_dict:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event_token,
                    messages =[TextMessage(text=Keywords_QA_dict[event_message])]
                )
            )
        
        if event_message in QA_dict:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event_token,
                    messages =[TextMessage(text=QA_dict[event_message])]
                )
            )
        
        if event_message == '面板-政策懶人包':
            temp_group = infos_carousel_groups.get_group('政策懶人包')
            carousel_template = Create_Template_Message(temp_group, fig_list)
            
            carousel_message = TemplateMessage(
                alt_text='XD',
                template=carousel_template
            )
        
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event_token,
                    messages =[carousel_message]
                )
            )
        
        elif event_message == '面板-政府官方網站':
            temp_group = infos_carousel_groups.get_group('政府官方網站')
            carousel_template = Create_Template_Message(temp_group, fig_list)
            
            carousel_message = TemplateMessage(
                alt_text='XD',
                template=carousel_template
            )
        
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event_token,
                    messages =[carousel_message]
                )
            )
        
        elif event_message == '面板-罰則':
            temp_group = infos_carousel_groups.get_group('罰則')
            carousel_template = Create_Template_Message(temp_group, fig_list)
            
            carousel_message = TemplateMessage(
                alt_text='XD',
                template=carousel_template
            )
        
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event_token,
                    messages =[carousel_message]
                )
            )
        
        elif event_message == '面板-綜合所得稅扣除額介紹':
            temp_group = infos_carousel_groups.get_group('綜合所得稅扣除額介紹')
            carousel_template = Create_Template_Message(temp_group, fig_list)
            
            carousel_message = TemplateMessage(
                alt_text='XD',
                template=carousel_template
            )
        
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event_token,
                    messages =[carousel_message]
                )
            )
        
        elif event_message == '面板-節稅':
            temp_group = infos_carousel_groups.get_group('節稅')
            carousel_template = Create_Template_Message(temp_group, fig_list)
            
            carousel_message = TemplateMessage(
                alt_text='XD',
                template=carousel_template
            )
        
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event_token,
                    messages =[carousel_message]
                )
            )

        qa_list = [f'{x[0]}\n{x[1]}' for x in keywords_df[['題目', '答案']].values if event_message in x[0]]
        num_qa_list = len(qa_list)
        if qa_list != 0:
            event_status = True

        if event_status:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event_token,
                    messages =[TextMessage(text=qa_list[random.randint(0, num_qa_list-1)])]
                )
            )
        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event_token,
                    messages =[TextMessage(text='查無\n請說明確一點')]
                )
            )

if __name__ == "__main__":
    app.run()


