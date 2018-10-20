#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import json


class Conversation:
    def __init__(self, messageDir, name):
        self.targetName = name
        self.messageDir = messageDir

        # Find the directory corresponding to that person
        name_plain = name.lower().replace(' ', '') + '_'
        convos = os.listdir(self.messageDir)
        targetDir = [dir for dir in convos if name_plain in dir]
        try:
            self.targetDir = targetDir[0]
        except IndexError:
            print('No matching conversation found in directory. Please try again.')
            return

        self.messagesPath = os.path.join(self.messageDir,
                                     self.targetDir,
                                     'message.json')

        with open(self.messagesPath, 'r') as f:
            messageJson = json.load(f)['messages']
        self.messages = pd.DataFrame(messageJson)

    def messages_over_time(self):
