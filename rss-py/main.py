#import redis
import feedparser
import os
import json
import re


url = 'http://farsi.khamenei.ir/rss'
response = feedparser.parse(url)
directory = "/var/log/py-report/"
os.system("mkdir " + directory)

for item in response.entries:
    year = "%d" % item.published_parsed.tm_year
    month = "%02d" % item.published_parsed.tm_mon
    day = "%02d" % item.published_parsed.tm_mday
    filedirectory = directory + year + "/" + month + "/" + day + "/"
    os.system("mkdir -p " + filedirectory)
    guid = re.findall("/(\d*)$", item.guid)[0]
    jsonfile = open(filedirectory + guid + ".json", "w")
    jsonfile.write(json.dumps(item))
    jsonfile.close()
