#!/usr/bin/python2.7

import re
import urllib2
from goose import Goose
from BeautifulSoup import BeautifulSoup
from webbrowser import open_new_tab

#open HTML file and write
filename = 'reading_estimator' + '.html' #i'll probably change the name
f = open(filename,'w')
HTMLhead = """<!DOCTYPE HTML>
<html>
<head><meta charset="UTF-8">
<title>Reading estimator</title></head>
<body><ol>
"""
f.write(HTMLhead)

def wordcount(value):
	# Find all non-whitespace patterns.
	list = re.findall("(\S+)", value)
    	# Return length of resulting list.
	return len(list)

def estimatedTime (text, speed):
        minutes = text / speed
        read_time =  str(minutes) + " minutes"
        return read_time

def wrapStringInHTML(title, read_time, url):
	wrapper = """ 
	<p><li><b> %s </b> - <i> %s </i><br>
	URL: <a href=\"%s\">%s</li></a></p>
	"""
	whole = wrapper % (title, read_time, url, url)
	return whole

def sourcePage (source_link): # source page where we will get links
	average_speed =180    #in wpm - could change to 1K char/min (function would also need to change)
	html_page = urllib2.urlopen(source_link)
	soup = BeautifulSoup(html_page)

	import datetime

	now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S") #i'll want this to append at the end of the html file to keep track of latest update

	for link in  soup.findAll('a', attrs={'href': re.compile("^http")}): # also gets https
		try:
			url = link.get('href')
			g = Goose()
			article = g.extract(url=url)

			dataInHTML = wrapStringInHTML((article.title), estimatedTime(wordcount(article.cleaned_text), average_speed), url) #this line is ridiculous.
			f.write(dataInHTML.encode('utf-8'))

			print article.title
			print estimatedTime(wordcount(article.cleaned_text), average_speed)
			print link.get('href')
			print ("\n")

		except IndexError:
			pass
		continue

	#f.write("Last update:%s", % now)  --> I still need to format this correctly

sourcePage("https://news.ycombinator.com/")
#sourcePage("https://lobste.rs/")


HTMLfooter = """</ol></body>
</html>
"""
f.write(HTMLfooter)
f.close()
open_new_tab(filename)

