import redis
import feedparser
import os
import json
import re
import .EmailAgent


def main():
    url = 'http://farsi.khamenei.ir/rss'
    response = feedparser.parse(url)
    directory = "/var/log/py-report/"
    os.system("mkdir " + directory)
    redisclient = redis.Redis()

    for item in response.entries:
        guid = re.findall("/(\d*)$", item.guid)[0]
        if(redisclient.sadd("items", guid)):
            year = "%d" % item.published_parsed.tm_year
            month = "%02d" % item.published_parsed.tm_mon
            day = "%02d" % item.published_parsed.tm_mday
            filedirectory = directory + year + "/" + month + "/" + day + "/"
            os.system("mkdir -p " + filedirectory)
            jsonfile = open(filedirectory + guid + ".json", "w")
            jsonfile.write(json.dumps(item))
            jsonfile.close()
            sendnew(item)

def sendnew(self, item):
    with open("configfile.txt", "r") as configfile:
        host = configfile.readline()
        port = configfile.readline()
        username = configfile.readline()
        password = configfile.readline()
        destination = configfile.readline()
        configfile.close()
        agent = EmailAgent(host, port, username, password)

        subject = 'New news is available'
        body =
            'title ' + item.title + '\n'
            + 'link' + item.link + '\n'
            + 'description' + item.description

        agent.send(username, destination, subject, body)

