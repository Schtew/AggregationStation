#!/bin/env python

from dotenv import load_dotenv
load_dotenv()

import os, mediacloud.api
import json

API_KEY = os.getenv('MEDIACLOUD_API')

testid = 1947
storylimit = 100

mc = mediacloud.api.MediaCloud(API_KEY)

topic = mc.topic(testid)

topiclist = mc.topicList()

with open("json/{0}.json".format(testid), "w") as file:
    json.dump(topic, file)

storylist = mc.topicStoryList(testid, limit=storylimit)
with open("json/testing.json", "w") as file:
    json.dump(storylist, file)

for x in stories:
    stories[x]["title"]
