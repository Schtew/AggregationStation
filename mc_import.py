#!/bin/env python

from dotenv import load_dotenv
load_dotenv()

import os, mediacloud.api

API_KEY = os.getenv('MEDIACLOUD_API')
testurl = "https://www.washingtonpost.com/politics/courts_law/supreme-court-census-undocumented-immigrants/2020/10/16/cf8288be-0f51-11eb-8074-0e943a91bf08_story.html"

mc = mediacloud.api.MediaCloud(API_KEY)

print(mc.stats())

print('test')