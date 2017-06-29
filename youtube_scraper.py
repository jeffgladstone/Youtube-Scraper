
"""
    Filename: youtube_scraper.py
    Author: Jeff Gladstone
    Date: 6/28/2017
    Description:
    This program parses HTML from individual Youtube video pages 
    to create a dictionary with title and views, which is 
    then sorted by view count. It inputs url extensions from 
    a CSV file called "url_extensions.csv" and outputs results 
    to an XML document called "youtube_output.xml".
"""

from lxml import html
import requests
import csv

# create list of url extensions from input file 'url_extensions.csv'
extensions = list()
with open("url_extensions.csv", "rt") as f:
	reader = csv.reader(f, delimiter=' ')
	for row in reader:
		extensions.append(row[0])

# initialize two lists: 'titles' and 'views'
vids = dict()

# iterate through url extensions and parse HTML to get video title and views
for extension in extensions:
	url = 'https://www.youtube.com/watch?v=' + extension
	page = requests.get(url)
	tree = html.fromstring(page.content)
	
	try:
		title = tree.xpath('//span[@id="eow-title"]/text()')[0]
		title = title.replace('\n    ', '').replace('\n  ', '')
		views = tree.xpath('//div[@class="watch-view-count"]/text()')[0]
		views = int(views.replace(' views', '').replace(',', ''))
		vids[extension] = {'title': title, 'views': views}	
	except:
		print('Video information not found. Try again.')
		print()

# sort videos by view count and prints list to console
vids = (sorted(vids.items(),key=lambda x: x[1]['views'], reverse = True))
print(vids)

# Write to output
with open("youtube_output.xml", "w") as f:
	for ext, vid in vids:
		f.write("<video>\n")
		f.write("\t<title>" + vid['title'] + "</title>\n")
		f.write("\t<views>" + str(vid['views']) + "</views>\n")
		f.write("</video>\n")