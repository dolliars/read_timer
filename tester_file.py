#!/usr/bin/python2.7

import re
import urllib2
import datetime
from goose import Goose
from BeautifulSoup import BeautifulSoup
from webbrowser import open_new_tab

#open HTML file and write
#file name separated, may change soon

filename = 'reading_estimator' + '.html'
f = open(filename,'w')

#HTML code
HTMLhead = """<!DOCTYPE HTML>
<html>
<head><meta charset="UTF-8">
<link rel="stylesheet" type="text/css" href="style.css">
<title>Reading estimator</title></head>
<body><ol>
"""
f.write(HTMLhead)

#list of links that will be excluded
exclude = ['http://www.ycombinator.com','https://github.com/HackerNews/API','http://www.ycombinator.com/apply/']

def wordcount(value):
	# Find all non-whitespace patterns.
	list = re.findall("(\S+)", value)
    	# Return length of resulting list.
	return len(list)

def estimatedTime (text, speed):
        minutes = text / speed
        read_time =  str(minutes) + " minutes"
        return read_time

def wrapStringInHTML(title, read_time, url, domain):
	wrapper = """ 
	<p><li><b><a href=\"%s\" target="_blank"> %s </a></b><br>
        <i> %s </i> - <a href=\"%s\">%s</li></a></p>
	"""
	whole = wrapper % (url, title, read_time, url, domain)
	return whole

def sourcePage (source_link):  # source page where we will get links
	average_speed = 180    #in wpm - could change to 1K char/min (function would also need to change)
	html_page = urllib2.urlopen(source_link)
	soup = BeautifulSoup(html_page)
        now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S") 

	for link in soup.findAll('a', attrs={'href': re.compile("^http")}):

            try:
                url = link.get('href')
                if url in exclude:
                    pass
                else:
                    g = Goose()
                    article = g.extract(url=url)
                    domain = article.domain

                    if not article.title:
                        article.title = url

		    dataInHTML = wrapStringInHTML((article.title), estimatedTime(wordcount(article.cleaned_text), average_speed), url, domain) #this line is ridiculous.
		    f.write(dataInHTML.encode('utf-8')) 

		    print article.title
		    print estimatedTime(wordcount(article.cleaned_text), average_speed)
		    print link.get('href')
		    print ("\n")
                     
            except IndexError:
                pass
            continue

        f.write("</ol>Last update: ")
        f.write(now)  

sourcePage("https://news.ycombinator.com/")
#sourcePage("https://lobste.rs/")

HTMLfooter = """</body>
</html>
"""
f.write(HTMLfooter)
f.close()
open_new_tab(filename)

