#!/bin/env python

from dotenv import load_dotenv
load_dotenv()

import os, mediacloud.api
import json

API_KEY = os.getenv('MEDIACLOUD_API')

testurl = "https://www.washingtonpost.com/world/the_americas/mexico-cartels-drugs-indictments/2020/10/17/101e1f06-0fe7-11eb-b404-8d1e675ec701_story.html"
testtitle = "Spanning years during drug wars, U.S. indictments claim cartels had reach into Mexico’s top security ranks"
testid = 1741917123

mc = mediacloud.api.MediaCloud(API_KEY)

# somehow need to take URL and convert it to story_id


story = mc.story(testid)

with open("{0}.json".format(testid), "w") as file:
    json.dump(story, file)

print(story)
