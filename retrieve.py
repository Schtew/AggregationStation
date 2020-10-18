#!/bin/env python

from dotenv import load_dotenv
load_dotenv()

import os, mediacloud.api
import json
from datetime import datetime

class Retrieve:
    def retrieve(self):
        API_KEY = os.getenv('MEDIACLOUD_API')

        testid = 1947
        storylimit = 100

        mc = mediacloud.api.MediaCloud(API_KEY)

        dateTimeObj = datetime.now()
        timestamp = dateTimeObj.strftime("%Y-%m-%d-%H-%M")

        topic = mc.topic(testid)
        topiclist = mc.topicList()

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

        return "json/query_{0}.json".format(timestamp)
