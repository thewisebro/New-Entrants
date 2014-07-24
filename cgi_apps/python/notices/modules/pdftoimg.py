#!/usr/bin/python

import re,os
from BeautifulSoup import BeautifulSoup

PeopleProxyUrl = "http://people.iitr.ernet.in/Notices/"

def replaceWithContents(element,imglocation):
	ix= element.parent.contents.index(element)
	for child in reversed(element.contents):
		showimage = "<img src=\""+PeopleProxyUrl+"userfiles/pdfimages/"+imglocation+".png\">"
		element.parent.insert(ix,showimage)
	element.extract()

def pdftoimg(html):
	#find ".pdf" in a string
	match = re.compile('\.(pdf)')

	# parse page content
	soup = BeautifulSoup(html)

	# check links
	for link in soup.findAll('a'):
		try:
			link['href'] = link['href'].replace('%20',' ')
			href = link['href']
			if re.search(match, href):
				filename = os.path.splitext(os.path.basename(href))[0]
				location = re.split(PeopleProxyUrl,href)[1]
				cmd = "convert -append -density 300 -resize 1024x -trim '"+location+"' -quality 100 -sharpen 0x1.0 'userfiles/pdfimages/"+filename+".png'"
				#os.system(cmd)
				replaceWithContents(link,filename)
		except Exception,e:
			pass
	
	print str(soup)
	
string = """<p>
<a href=" """+PeopleProxyUrl+"""userfiles/files/Self_Study_Notice.pdf">http://people.iitr.ernet.in/Notices/userfiles/files/Self_Study_Notice.pdf</a></p>"""

pdftoimg(string)

