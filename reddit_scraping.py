#!/usr/bin/python

#############################################################
# File Name: reddit_scraping.py
# Purpose: Scrape Reddit and Re-post Images to Facebook & Twitter
# Created by: Corey Sykes
# Modifications:
# --------------
# Date           Updated By    Comments
# -----          -----------   ------------------------------
# 01-May-2017    Corey Sykes   Created
#############################################################

import praw
import facebook
import pymysql
import twitter
import time
import requests
import random



#Creating a function to download each image and store it on the local drive, so we can upload it
#to Facebook and Twitter. We keep the same file name, because it's a temporary file - no need to change it.
def downloadImage(imageUrl, localFileName):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        print('Downloading %s...' % (localFileName))
        with open(localFileName, 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)
				
				
#Connecting to the Facebook, Reddit, and Twitter APIs
#with the Access Token & Secret information
aww_graph = facebook.GraphAPI(access_token)
aww_reddit = praw.Reddit(client_id, client_secret, password, user_agent, username)
aww_twitter = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)

#Opening a connection to our local MySQL instance (hosted by XAMPP)
#Here I've stored all distinct pages that I've posted on Facebook and Twitter, so I don't duplicate posting
aww_conn = pymysql.connect(host = "localhost", user="root", db="reddit_to_fb_scraping")
aww_cur = aww_conn.cursor()

#Writing a query to grab all of the distinct pages and append it to a list, so we can check against the list when we're
#trying to grab new URLs
aww_query = "SELECT DISTINCT URL FROM aww_urls"
aww_cur.execute(aww_query)
aww_result = aww_cur.fetchall()
aww_posted_url_list = []
for row in aww_result:
    aww_posted_url_list.append(row[0])

#Writing a lits of trends by using Twitter's GetTrendsWoeid() function. This will show me the top 20 Twitter Hashtags currently
#for the USA
trends = []
trends_list = aww_twitter.GetTrendsWoeid(23424977)
for topic in trends_list:
        if "#" in topic.name:
            trends.append(topic.name)
trends = [item.encode('utf-8') for item in trends]

#Writing a loop to connect into Reddit's API and choosing a specific subreddit and topic (hot, top, comments)
#Then checking for an image to be in the url (ending in JPG or PNG)
#Then checking if that URL is in our previously posted list in our MySQL database
#If we get through this, we try to post it to Twitter and Facebook.
#For twitter, we grab a random integer between 1 and the length of the trends list (top hashtags on Twitter at the moment)
#then we just use the PostUpdate() function to post that URL with the hashtag (trying to get more exposure)
#For Facebook, we use our downloadImage() function we made to download the photo temporarily and then to post it with the
#URL and Title of the post.
for submission in aww_reddit.subreddit('aww').hot(limit=None):
    if ("jpg" in submission.url) or ("png" in submission.url):
        if not submission.url in aww_posted_url_list:
            try:
                rand = random.randint(0, len(trends))
                aww_twitter.PostUpdate(trends[rand],media=submission.url)
                localFileName = 'C:\\Users\\cosykes\\side_project\\aww_photos\\reddit_aww_image_download_temp.jpg'
                downloadImage(submission.url, localFileName)
                content_to_post = submission.url
                title_to_post = submission.title
                aww_graph.put_photo(image=open(localFileName, 'rb'), message=submission.title)
                aww_posted_url_list.append(submission.url)
            except:
                pass
            aww_posted_url_list.append(submission.url)
            time.sleep(15)

#Repeating for the Aww Subreddit & Top (Limit None)
for submission in aww_reddit.subreddit('aww').top(limit=None):
    if ("jpg" in submission.url) or ("png" in submission.url):
        if not submission.url in aww_posted_url_list:
            try:
                rand = random.randint(0, len(trends))
                aww_twitter.PostUpdate(trends[rand],media=submission.url)
                localFileName = 'C:\\Users\\cosykes\\side_project\\aww_photos\\reddit_aww_image_download_temp.jpg'
                downloadImage(submission.url, localFileName)
                content_to_post = submission.url
                title_to_post = submission.title
                aww_graph.put_photo(image=open(localFileName, 'rb'), message=submission.title)
                aww_posted_url_list.append(submission.url)
            except:
                pass
            aww_posted_url_list.append(submission.url)
            time.sleep(15)          

#Repeating for the Aww Subreddit & Rising (Limit None)
for submission in aww_reddit.subreddit('aww').rising(limit=None):
    if ("jpg" in submission.url) or ("png" in submission.url):
        if not submission.url in aww_posted_url_list:
            try:
                rand = random.randint(0, len(trends))
                aww_twitter.PostUpdate(trends[rand],media=submission.url)
                localFileName = 'C:\\Users\\cosykes\\side_project\\aww_photos\\reddit_aww_image_download_temp.jpg'
                downloadImage(submission.url, localFileName)
                content_to_post = submission.url
                title_to_post = submission.title
                aww_graph.put_photo(image=open(localFileName, 'rb'), message=submission.title)
                aww_posted_url_list.append(submission.url)
            except:
                pass
            time.sleep(15)
            aww_posted_url_list.append(submission.url)
			
#Printing out how many pages I've posted
print(len(aww_posted_url_list))

#Writing all of the new posted pages into my current database
aww_conn = pymysql.connect(host = "localhost", user="root", db="reddit_to_fb_scraping")
aww_cur = aww_conn.cursor()
for row in aww_posted_url_list:
    aww_cur.execute("INSERT INTO `aww_urls` VALUES ('%s')" % row)
    aww_conn.commit()
	
#Creating and dropping temporary tables to my production version
time.sleep(5)
aww_cur.execute("DROP TABLE aww_temp")
aww_conn.commit()
time.sleep(15)
aww_cur.execute("CREATE TABLE aww_temp AS SELECT DISTINCT URL FROM aww_urls")
aww_conn.commit()
time.sleep(15)
aww_cur.execute("DROP TABLE aww_urls")
aww_conn.commit()
time.sleep(15)
aww_cur.execute("CREATE TABLE aww_urls AS SELECT DISTINCT URL FROM aww_temp")
aww_conn.commit()
time.sleep(15)