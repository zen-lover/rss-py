import redis
import feedparser
import os
import json
import re
import logging
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    # make directory with linux command with python os library
    os.system("mkdir " + "/var/log/py_log")
    # get current time of system
    x = datetime.datetime.now()
    date = x.strftime("%Y") + x.strftime("%m") + x.strftime("%d") + \
           x.strftime("%H") + x.strftime("%M") + x.strftime("%S")
    # set configuration for logging events of program
    logging.basicConfig(level=logging.DEBUG, filename="/var/log/py_log/" + date + ".log", filemode='w')
    logger = logging.getLogger()
    # url address for get response from it
    url = 'http://farsi.khamenei.ir/rss'
    response = feedparser.parse(url)
    # make directory for save report with linux command with python os library
    directory = "/var/log/py_report/"
    os.system("mkdir " + directory)
    # create a redis database for saving data and always can use it
    redisclient = redis.Redis()

    # iteration on items of response from url
    for item in response.entries:
        # define id for item from it's body
        guid = re.findall("/(\d*)$", item.guid)[0]
        # check in database that whether this item already exist or not
        if redisclient.sadd("items", guid):
            logger.info('new news is available')
            year = "%d" % item.published_parsed.tm_year
            month = "%02d" % item.published_parsed.tm_mon
            day = "%02d" % item.published_parsed.tm_mday
            filedirectory = directory + year + "/" + month + "/" + day + "/"
            os.system("mkdir -p " + filedirectory)
            jsonfile = open(filedirectory + guid + ".json", "w")
            jsonfile.write(json.dumps(item))
            jsonfile.close()
            # send email for this item
            sendnew(item)
            logger.info('email sent')


def sendnew(item):
    # read information from config file
    with open("configfile.txt", "r") as configfile:
        host = configfile.readline()
        port = int(configfile.readline())
        username = configfile.readline()
        password = configfile.readline()
        destination = configfile.readline()
        configfile.close()

        subject = 'New news is available'

        # create body of email that contains title, link and description
        body = \
            'title ' + item.title + '\n' \
            + 'link' + item.link + '\n' \
            + 'description' + item.description

        # create a agent that can send email
        smtp = smtplib.SMTP(host, port)
        smtp.starttls()
        smtp.login(username, password)

        # Create a message
        message = MIMEMultipart()

        # Setup the parameters of the message
        message['From'] = username
        message['To'] = destination
        message['Subject'] = subject

        # Add in the message body
        message.attach(MIMEText(body.encode('utf-8'), 'plain'))

        # Sendding the message
        smtp.send_message(message)
        smtp.quit()


if __name__ == '__main__':
    main()
