import pandas as pd
from collections import Counter
import collections
import re
import operator
import json
import nltk
from nltk.corpus import stopwords
import matplotlib

import matplotlib.pyplot as plt

with open('result.json') as json_data:

    data = json.load(json_data)
    targetChatIds = [8, 50];
    chats = [];

    for chatId in targetChatIds:
        chats += data['chats']['list'][chatId]['messages']

    for index, chat in enumerate(data['chats']['list']):
        if('name' in chat) and chat['name'] is not None:
            print(str(index) + " | " + chat['name'])

    no_percent = lambda chat: 'service' not in chat['type']
    chatMessages = filter(no_percent, chats)

    # Person Message Count
    personMessageCount = Counter(chat['from'] for chat in chatMessages).items()
    print(type(personMessageCount))
    for name, msgCount in personMessageCount:
        print(name + ":\n" + str(msgCount) + " messages \n")

    # Most used words
    messages = map(lambda value: value['text'], chatMessages)
    words = re.findall(r'\w+', str(messages).lower())
    common = Counter(words).most_common(80000)
    stopwords = stopwords.words('dutch')
    stopwords.extend(('type', 'text', 'we', 'wel', 'n', 'mention', 'language', 'link', 'https', 'p', 'd', 'com'))
    importantWords = []
    for word, wordCount in common:
        if word not in stopwords:
            importantWords.append(tuple((word, wordCount)))

    # print(importantWords)

    # Time
    timestamps = map(lambda value: value['date'], chatMessages)
    
    timestampDataFrame = pd.DataFrame({'date': timestamps})
    timestampDataFrame["date"] = timestampDataFrame["date"].astype("datetime64")
    # byYear = timestampDataFrame.groupby(timestampDataFrame["date"].dt.year).count().plot(kind="bar")
    # byMonth = timestampDataFrame.groupby([timestampDataFrame["date"].dt.year, timestampDataFrame["date"].dt.month]).count().plot(kind="bar")
    # byMonthCumulative = timestampDataFrame.groupby(timestampDataFrame["date"].dt.month).count().plot(kind="bar")
    # byDayCumulative = timestampDataFrame.groupby([timestampDataFrame["date"].dt.day]).count().plot(kind="bar")
    # byHourCumulative = timestampDataFrame.groupby([timestampDataFrame["date"].dt.hour]).count().plot(kind="bar")

    plt.title('Group activity')
    plt.xlabel('Date')
    plt.ylabel('Messages')
    plt.legend(['Messages'])
    plt.grid(alpha=0.3)
    plt.show()
