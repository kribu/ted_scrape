#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import codecs

# Filename is the file you save the results into.
filename = "ted_talks.csv"
f = codecs.open(filename, "w", "utf-8")
headers = "name, title, date, rate\n"
f.write(headers)

# TED page doesn't allow many queries at once. Must do in patches.
for i in range(1, 11):
	my_url = 'https://www.ted.com/talks?page=%s'%str(i)

	uClient = uReq(my_url) #open connection
	page_html = uClient.read() #save it as a variable, raw html
	uClient.close() #close the connection

	#html parsing
	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll("div", {"class":"media__message"})

	for container in containers:
		name = container.h4.text.strip()
		title = container.a.text.strip()
		date = container.span.span.text.strip()

		rate_container = container.findAll("span", {"class":"meta__row"})
		if len(rate_container) == 0:
			rate = "NA"
		else:
			rate = rate_container[0].span.text.strip()

		f.write(name.replace(",", "|") + "," + title.replace(",", "|") + "," + date + "," + rate.replace(",", ".") +"\n")

f.close()
