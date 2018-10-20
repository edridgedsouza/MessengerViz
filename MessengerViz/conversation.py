#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from ggplot import *
import os
import json
from datetime import datetime as dt
from helpers import Helpers


class Conversation:
    def __init__(self, messageDir, name):
        self.BLOCK = 7

        self.targetName = name
        self.messageDir = messageDir

        # Find the directory corresponding to that person
        name_plain = name.lower().replace(' ', '') + '_'
        convos = os.listdir(self.messageDir)
        targetDir = [dir for dir in convos if name_plain in dir]
        try:
            self.targetDir = targetDir[0]
        except IndexError:
            print('No matching conversation found in directory.')
            print('Please try again.')
            return

        self.messagesPath = os.path.join(self.messageDir,
                                         self.targetDir,
                                         'message.json')

        with open(self.messagesPath, 'r') as f:
            messageJson = json.load(f)['messages']
        self.messages = pd.DataFrame(messageJson)
        self.messages['timestamp'] = self.messages.timestamp_ms.map(lambda x:
            dt.fromtimestamp(x/1000.0))
        self.messages['Year'] = self.messages.timestamp.map(lambda x: x.year)
        self.messages['Month'] = self.messages.timestamp.map(lambda x: x.month)
        self.messages['Day'] = self.messages.timestamp.map(lambda x: x.day)
        self.messages['Hour'] = self.messages.timestamp.map(lambda x: x.hour)
        self.messages['Minute'] = self.messages.timestamp.map(lambda x:
                                                              x.minute)
        self.messages['Second'] = self.messages.timestamp.map(lambda x:
                                                              x.second)
        self.messages['DayOfWeek'] = self.messages.timestamp.map(lambda x:
                                                                 x.dayofweek)

    def messages_over_time(self, aggregate='messages'):
        """
        Plot messages by both senders over time. Choose whether you want to
        aggregate them by number of messages or by volume of messages.
        The parameter `aggregate` takes either 'messages' or 'volume'.
        """
        messages = self.messages.copy()
        if aggregate.lower() == 'messages':
            messages = (messages.groupby(['Year', 'Month', 'Day', 'sender_name'])
                        .agg({'content':'count'}).reset_index())
            messages['Date'] = Helpers.makeDatetime(messages)
            print(messages)
            g = ggplot(messages, aes('Date','content',
                                     fill='sender_name'))
            g = g + geom_area(position = 'stack') + Helpers.ggplot_theme()
            print(g)
        elif aggregate.lower() == 'volume':
            pass
