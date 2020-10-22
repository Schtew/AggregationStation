import mediacloud.api
import os
from datetime import datetime

from dotenv import load_dotenv


class Retrieve:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('MEDIACLOUD_API')
        self.mc = mediacloud.api.MediaCloud(self.API_KEY)

    def genMetrics(self, title=None, media_name=None, author=None, url=None, age=None, inlink_count=None,
                   outlink_count=None, facebook_share_count=None, polarity=None, subjectivity=None, bias=None,
                   credibility=None, l_c=None, tags=None):
        metrics = {
            "title": title,
            "media_name": media_name,
            "author": author,
            "url": url,
            "metrics": {
                "age": age,
                "inlink_count": inlink_count,
                "outlink_count": outlink_count,
                "facebook_share_count": facebook_share_count,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "bias": bias,
                "credibility": credibility,
                "liberal/conservative": l_c,
                "tags": tags
            }
        }
        return metrics

    def collectionAnalyze(self, mc, storylimit, timestamp):
        storylist = mc.storyList(solr_query="tags_id_media:34412282",
                                 solr_filter="publish_day:[2020-10-10T00:00:00Z TO 2020-12-20T00:00:00Z]",
                                 rows=storylimit)

        resources = {"articles": []}
        for index, value in enumerate(storylist):
            if value["publish_date"] != "undateable":
                value["publish_date"] = value["publish_date"][:19]
                difference = (datetime.strptime(timestamp, "%Y-%m-%d-%H-%M") - datetime.strptime(
                    value["publish_date"], "%Y-%d-%m %H:%M:%S")).total_seconds()
                difference = int(difference)
                if difference < 0:
                    difference = None

            taglist = []
            for tag in value["story_tags"]:
                taglist.append(tag["tag"])

            metrics = self.genMetrics(age=difference, tags=taglist, media_name=value["media_name"], url=value["url"])
            resources["articles"].append(metrics)

        return resources

    def topicAnalyze(self, mc, storylimit, timestamp, testid):
        storylist = mc.topicStoryList(testid, limit=storylimit)

        resources = {"articles": []}
        for index, value in enumerate(storylist["stories"]):
            if value["publish_date"] != "undateable":
                difference = (datetime.strptime(timestamp, "%Y-%m-%d-%H-%M") - datetime.strptime(
                    value["publish_date"], "%Y-%m-%d %H:%M:%S")).total_seconds()
                difference = int(difference)
            else:
                difference = None
            if value["media_name"] == "Twitter" and value["media_name"] != "hashtag":
                author = "@{0}".format(value["url"].split("/")[3])
            else:
                author = None

            metrics = self.genMetrics(age=difference, inlink_count=value["inlink_count"], outlink_count=value["outlink_count"], facebook_share_count=value["facebook_share_count"],
                                      title=value["title"], media_name=value["media_name"], author=author, url=value["url"])

            resources["articles"].append(metrics)

        return resources

    def retrieve(self, timestamp, testid=1947, storylimit=10, topicBool=False):
        if topicBool:
            return self.topicAnalyze(self.mc, storylimit, timestamp, testid)
        else:
            return self.collectionAnalyze(self.mc, storylimit, timestamp)
