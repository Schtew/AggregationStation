#!/bin/env python

from dotenv import load_dotenv
load_dotenv()

import os, mediacloud.api
import json
from datetime import datetime

class Retrieve:
    def retrieve(self, storylimit=10):
        API_KEY = os.getenv('MEDIACLOUD_API')

        testid = 1947

        topic = False   # set this for false if using a media collection

        mc = mediacloud.api.MediaCloud(API_KEY)

        dateTimeObj = datetime.now()
        timestamp = dateTimeObj.strftime("%Y-%m-%d-%H-%M")

        topic = mc.topic(testid)
        topiclist = mc.topicList()

        if topic == True:
            storylist = mc.topicStoryList(testid, limit=storylimit)

            resources = {"articles": []}
            for index, value in enumerate(storylist["stories"]):
                if value["publish_date"] != "undateable":
                    difference = (datetime.strptime(timestamp, "%Y-%m-%d-%H-%M") - datetime.strptime(value["publish_date"], "%Y-%m-%d %H:%M:%S")).total_seconds()
                    difference = int(difference)
                else:
                    difference = None
                if value["media_name"] == "Twitter" and value["media_name"] != "hashtag":
                    author = "@{0}".format(value["url"].split("/")[3])
                else:
                    author = None

                metrics = {
                    "age": difference,
                    "inlink_count": value["inlink_count"],
                    "outlink_count": value["outlink_count"],
                    "facebook_share_count": value["facebook_share_count"]
                }
                templink = {
                    "title": value["title"],
                    "media_name": value["media_name"],
                    "author": author,
                    "url": value["url"],
                    "metrics": metrics}
                resources["articles"].append(templink)

            with open("json/query_{0}.json".format(timestamp), "w") as file:
                json.dump(resources, file)

            return resources
        else:
            params = {'q': 'tags_id_media:34412282'}
            storylist = mc.storyList(show_feeds=True, solr_query="tags_id_media:34412282", solr_filter="publish_day:[2020-10-01T00:00:00Z TO 2020-12-20T00:00:00Z]", rows=storylimit)
            with open("json/testing2.json", "w") as file:
                json.dump(storylist, file)
            resources = {"articles": []}
            for index, value in enumerate(storylist):
                if value["publish_date"] != "undateable":
                    difference = (datetime.strptime(timestamp, "%Y-%m-%d-%H-%M") - datetime.strptime(value["publish_date"], "%Y-%d-%m %H:%M:%S")).total_seconds()
                    difference = int(difference)
                    if difference < 0:
                        difference = None

                # dictvalues = {"conservative": 1, "liberal": 2}
                dictvalues[json["credibility"]] = 2
                metrics = {
                    "age": difference,
                }
                templink = {
                    "title": None,
                    "media_name": value["media_name"],
                    "author": None,
                    "url": value["guid"],
                    "metrics": metrics}
                resources["articles"].append(templink)

            with open("json/query_{0}.json".format(timestamp), "w") as file:
                json.dump(resources, file)

            return resources
p = Retrieve()
p.retrieve()