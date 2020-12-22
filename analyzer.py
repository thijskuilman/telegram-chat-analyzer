import json
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import re

chatMessages = [];

def import_json():
	global chatMessages
	# Get chat data
	with open('result.json', encoding="utf8") as json_data:
	  data = json.load(json_data)
	chatData = data['chats']['list'];
	for index, chat in enumerate(chatData):
	    if('name' in chat) and chat['name'] is not None:
	        print("[" + str(index) + "] " + chat['name'])
	# Ask for chat IDs
	user_input = input("Enter the chat ID indices, separated by commas: ")
	input_list = user_input.split(',')
	chatIds = [int(x.strip()) for x in input_list]
	# Analyzed chats
	for chatId in chatIds:
		chatMessages += chatData[chatId]['messages']
	# Parse chat messages
	no_percent = lambda chat: 'service' not in chat['type']
	chatMessages = list(filter(no_percent, chatMessages))

def showMessagesPerPerson():
	global chatMessages
	personMessageCount = Counter(chat['from'] for chat in chatMessages).items()
	for name, msgCount in personMessageCount:
		if name:
			print(name + ":\n" + str(msgCount) + " messages \n")

def showMostUsedWords(amount):
	global chatMessages
	global stopwords
	messagesTexts = [];
	for message in chatMessages:
		messagesTexts.append(message['text'])
	words = re.findall(r'\w+', str(messagesTexts).lower())
	common = Counter(words).most_common(100000)
	stopwords = stopwords.words('dutch')
	stopwords.extend(('ok', 'ah', 'the', 'nl', 'echt', 'watch', 'v', 'goed', 'ga', 'oh', 'http', 'weet', 'denk', 'kun', 'www', 'type', 'text', 'we', 'wel', 'n', 'mention', 'language', 'link', 'https', 'p', 'd', 'com', 'a', 'aan', 'aangaande', 'aangezien', 'achter', 'achterna', 'aen', 'af', 'afd', 'afgelopen', 'agter', 'al', 'aldaar', 'aldus', 'alhoewel', 'alias', 'alle', 'allebei', 'alleen', 'alleenlyk', 'allen', 'alles', 'als', 'alsnog', 'altijd', 'altoos', 'altyd', 'ander', 'andere', 'anderen', 'anders', 'anderszins', 'anm', 'b', 'behalve', 'behoudens', 'beide', 'beiden', 'ben', 'beneden', 'bent', 'bepaald', 'beter', 'betere', 'betreffende', 'bij', 'bijna', 'bijvoorbeeld', 'bijv', 'binnen', 'binnenin', 'bizonder', 'bizondere', 'bl', 'blz', 'boven', 'bovenal', 'bovendien', 'bovengenoemd', 'bovenstaand', 'bovenvermeld', 'buiten', 'by', 'daar', 'daarheen', 'daarin', 'daarna', 'daarnet', 'daarom', 'daarop', 'daarvanlangs', 'daer', 'dan', 'dat', 'de', 'deeze', 'den', 'der', 'ders', 'derzelver', 'des', 'deszelfs', 'deszelvs', 'deze', 'dezelfde', 'dezelve', 'dezelven', 'dezen', 'dezer', 'dezulke', 'die', 'dien', 'dikwijls', 'dikwyls', 'dit', 'dl', 'doch', 'doen', 'doet', 'dog', 'door', 'doorgaand', 'doorgaans', 'dr', 'dra', 'ds', 'dus', 'echter', 'ed', 'een', 'eene', 'eenen', 'eener', 'eenig', 'eenige', 'eens', 'eer', 'eerdat', 'eerder', 'eerlang', 'eerst', 'eerste', 'eersten', 'effe', 'egter', 'eigen', 'eigene', 'elk', 'elkanderen', 'elkanderens', 'elke', 'en', 'enig', 'enige', 'enigerlei', 'enigszins', 'enkel', 'enkele', 'enz', 'er', 'erdoor', 'et', 'etc', 'even', 'eveneens', 'evenwel', 'ff', 'gauw', 'ge', 'gebragt', 'gedurende', 'geen', 'geene', 'geenen', 'gegeven', 'gehad', 'geheel', 'geheele', 'gekund', 'geleden', 'gelijk', 'gelyk', 'gemoeten', 'gemogen', 'geven', 'geweest', 'gewoon', 'gewoonweg', 'geworden', 'gezegt', 'gij', 'gt', 'gy', 'haar', 'had', 'hadden', 'hadt', 'haer', 'haere', 'haeren', 'haerer', 'hans', 'hare', 'heb', 'hebben', 'hebt', 'heeft', 'hele', 'hem', 'hen', 'het', 'hier', 'hierbeneden', 'hierboven', 'hierin', 'hij', 'hoe', 'hoewel', 'hun', 'hunne', 'hunner', 'hy', 'ibid', 'idd', 'ieder', 'iemand', 'iet', 'iets', 'ii', 'iig', 'ik', 'ikke', 'ikzelf', 'in', 'indien', 'inmiddels', 'inz', 'inzake', 'is', 'ja', 'je', 'jezelf', 'jij', 'jijzelf', 'jou', 'jouw', 'jouwe', 'juist', 'jullie', 'kan', 'klaar', 'kon', 'konden', 'krachtens', 'kunnen', 'kunt', 'laetste', 'lang', 'later', 'liet', 'liever', 'like', 'm', 'maar', 'maeken', 'maer', 'mag', 'martin', 'me', 'mede', 'meer', 'meesten', 'men', 'menigwerf', 'met', 'mezelf', 'mij', 'mijn', 'mijnent', 'mijner', 'mijzelf', 'min', 'minder', 'misschien', 'mocht', 'mochten', 'moest', 'moesten', 'moet', 'moeten', 'mogelijk', 'mogelyk', 'mogen', 'my', 'myn', 'myne', 'mynen', 'myner', 'myzelf', 'na', 'naar', 'nabij', 'nadat', 'naer', 'net', 'niet', 'niets', 'nimmer', 'nit', 'no', 'noch', 'nog', 'nogal', 'nooit', 'nr', 'nu', 'o', 'of', 'ofschoon', 'om', 'omdat', 'omhoog', 'omlaag', 'omstreeks', 'omtrent', 'omver', 'onder', 'ondertussen', 'ongeveer', 'ons', 'onszelf', 'onze', 'onzen', 'onzer', 'ooit', 'ook', 'oorspr', 'op', 'opdat', 'opnieuw', 'opzij', 'opzy', 'over', 'overeind', 'overigens', 'p', 'pas', 'pp', 'precies', 'pres', 'prof', 'publ', 'reeds', 'rond', 'rondom', 'rug', 's', 'sedert', 'sinds', 'sindsdien', 'sl', 'slechts', 'sommige', 'spoedig', 'st', 'steeds', 'sy', 't', 'tamelijk', 'tamelyk', 'te', 'tegen', 'tegens', 'ten', 'tenzij', 'ter', 'terwijl', 'terwyl', 'thans', 'tijdens', 'toch', 'toe', 'toen', 'toenmaals', 'toenmalig', 'tot', 'totdat', 'tusschen', 'tussen', 'tydens', 'u', 'uit', 'uitg', 'uitgezonderd', 'uw', 'uwe', 'uwen', 'uwer', 'vaak', 'vaakwat', 'vakgr', 'van', 'vanaf', 'vandaan', 'vanuit', 'vanwege', 'veel', 'veeleer', 'veelen', 'verder', 'verre', 'vert', 'vervolgens', 'vgl', 'vol', 'volgens', 'voor', 'vooraf', 'vooral', 'vooralsnog', 'voorbij', 'voorby', 'voordat', 'voordezen', 'voordien', 'voorheen', 'voorop', 'voort', 'voortgez', 'voorts', 'voortz', 'vooruit', 'vrij', 'vroeg', 'vry', 'waar', 'waarom', 'wanneer', 'want', 'waren', 'was', 'wat', 'we', 'weer', 'weg', 'wege', 'wegens', 'weinig', 'weinige', 'wel', 'weldra', 'welk', 'welke', 'welken', 'welker', 'werd', 'werden', 'werdt', 'wezen', 'wie', 'wiens', 'wier', 'wierd', 'wierden', 'wij', 'wijzelf', 'wil', 'wilde', 'worden', 'wordt', 'wy', 'wyze', 'wyzelf', 'zal', 'ze', 'zeer', 'zei', 'zeker', 'zekere', 'zelf', 'zelfde', 'zelfs', 'zelve', 'zelven', 'zelvs', 'zich', 'zichzelf', 'zichzelve', 'zichzelven', 'zie', 'zig', 'zij', 'zijn', 'zijnde', 'zijne', 'zijner', 'zo', 'zo', 'zoals', 'zodra', 'zommige', 'zommigen', 'zonder', 'zoo', 'zou', 'zoude', 'zouden', 'zoveel', 'zowat', 'zulk', 'zulke', 'zulks', 'zullen', 'zult', 'zy', 'zyn', 'zynde', 'zyne', 'zynen', 'zyner', 'zyns'))
	importantWords = []
	for word, wordCount in common:
	    if word not in stopwords:
	        importantWords.append(tuple((word, wordCount)))
	print(importantWords[:amount])

def showMessageGraph():
	global chatMessages
	timestamps = map(lambda value: value['date'], chatMessages)
	timestampDataFrame = pd.DataFrame({'date': timestamps})
	timestampDataFrame["date"] = timestampDataFrame["date"].astype("datetime64")
	byYear = timestampDataFrame.groupby(timestampDataFrame["date"].dt.year).count().plot(kind="bar")
	byMonth = timestampDataFrame.groupby([timestampDataFrame["date"].dt.year, timestampDataFrame["date"].dt.month]).count().plot(kind="bar")
	byHourCumulative = timestampDataFrame.groupby([timestampDataFrame["date"].dt.hour]).count().plot(kind="bar")
	plt.title('Group messages')
	plt.xlabel('Date')
	plt.ylabel('Messages')
	plt.legend(['Messages'])
	plt.grid(alpha=0.3)
	plt.show()

import_json();
showMostUsedWords(50);
showMessagesPerPerson();
showMessageGraph();
