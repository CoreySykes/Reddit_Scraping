# Reddit_Scraping
This repository houses a script used to scrape Reddit and re-post to Facebook & Twitter

### Overview

The purpose of this project was to develop Python skills. Even though I know Python and use it for work,
I work too much and don't leave enough time for side projects to show my skill-set. For this reason, I took a simple thought
and decided to code it out. I wanted to scrape Reddit's 'aww' section for new images and re-post those to a Facebook page
and Twitter as well.

### How to Run

You can't really download and run the script -- however, you can use it to mold your own. 
You'll need to import your own API keys & secrets for Reddit, Facebook, and Twitter, as well as setup your own local MySQL instance.

### Summary

The script does the following:

1. Creates a downloadImage() function to store images temporarily on a local machine
2. Creates a connection to Reddit, Facebook, and Twitter through their APIs.
3. Creates a connection to a local MySQL instance hosted on XAMPP.
4. Creates a list to check already posted pages (stored in MySQL).
5. Scrapes Reddit's Aww section in Hot, Top, and Rising with no limit.
6. Posts the image to Twitter & Facebook.