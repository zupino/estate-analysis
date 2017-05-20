#! /usr/bin/python

from lxml import html
import requests
import urllib
import json

# This is the page
host = "http://www.immobilienscout24.de"
page = requests.get(host + '/Suche/Wohnung-Kauf/Baden-Wuerttemberg/Stuttgart')
tree = html.fromstring(page.content)
# This rule will match 2 nodes, we use the first one as it contains only the number
numOfResults = tree.xpath('//span[@data-is24-qa="resultlist-resultCount"]/text()')

resPerPage = 20
i = 0

# Printing the headers for CSV file
print('"id","title","price","meters","rooms","address","area","link"')

for x in range(0, int(numOfResults[0])/resPerPage):
#for x in range(1, 5):
	
	if x == 0:
		page = requests.get(host + '/Suche/Wohnung-Kauf/Baden-Wuerttemberg/Stuttgart')
	else:
		page = requests.get(host + '/Suche/S-/P-' + str(x) +  '/Wohnung-Kauf/Baden-Wuerttemberg/Stuttgart')
				
	tree = html.fromstring(page.content)
	
	#titles    = tree.xpath('//ul[@id="resultListItems"]/li[not(contains(@class,"result-list__listing--xl"))]/article/div/div/div[contains(@class,"result-list-entry__data")]/a/h5/span[@result-list-entry__brand-title]/text()')
	#links     = tree.xpath('//ul[@id="resultListItems"]/li[not(contains(@class,"result-list__listing--xl"))]/article/div/div/div[contains(@class,"result-list-entry__data")]/a/@href')
	#details   = tree.xpath('//ul[@id="resultListItems"]/li[not(contains(@class,"result-list__listing--xl"))]/article/div/div/div/div/div/dl/dd/text()')
	#addresses = tree.xpath( '//ul[@id="resultListItems"]/li[not(contains(@class,"result-list__listing--xl"))]/article/div/div/div[contains(@class,"result-list-entry__data")]/div[contains(@class,"result-list-entry__address")]/span/text()' )
	
	titles    = tree.xpath('//li[not(contains(@class, "result-list__listing--xl"))]/article/div/div/div/a[contains(@class, "result-list-entry__brand-title-container")]/h5/text()')
	links     = tree.xpath('//li[not(contains(@class, "result-list__listing--xl"))]/article/div/div/div/a[contains(@class, "result-list-entry__brand-title-container")]/@href')
        details   = tree.xpath('//li[not(contains(@class, "result-list__listing--xl"))]/article[contains(@id, "result-")]/div/div/div/div/div/dl/dd/text()')
        addresses = tree.xpath('//li[not(contains(@class, "result-list__listing--xl"))]/article[contains(@id, "result-")]/div/div/div/div[contains(@class, "result-list-entry__address")]/span/text()')

#	print("\t[DEBUG] title contains " + str(titles.__len__()) + " elements")

	# This get the 
	i = 0
	apts = {}
	for p in titles:
		
		# details: 0 price, 1 meters, 2 rooms, 3 empty
		# links format: /expose/<id>
		
		# Prepare the correct format for the price
		priceRaw = details[(i*4)].strip().split()
		if priceRaw.__len__() > 2:
			price = int( ( int( priceRaw[0].replace(".", "").replace(",", "") ) + int(priceRaw[2].replace(".", "")) ) / 2 )
		elif priceRaw.__len__() == 2: 
			price = int( priceRaw[0].replace(".", "").replace(",", "") )
		else:
			price = "na"	
		
		# Same logic for the meters
		# Prepare the correct format for the price
		
		meterRaw = details[(i*4)+1].strip().split(" ")[0]
		meters = int( float( meterRaw.replace(",", ".") ) )
				
		# Similar logic and input check for rooms
		if details[(i*4)+2].strip().__len__() == 1:
			rooms = int(details[(i*4)+2].strip())
		elif details[(i*4)+2].strip().__len__() == 3:
			rooms = int( float( details[(i*4)+2].strip().replace(",", ".") ) )
		else:
			rooms = "na"
			
		# Adding the address to the fields
		if i < len(addresses):
			address = str(addresses[i].encode('utf-8').strip())
		else:
			address = "na"

		# Adding the area of the city (last 2 elements of the address, separated by comma
		if address.split(',').__len__() > 1:
			# GeoCoding!!
			geoReq = "https://maps.googleapis.com/maps/api/geocode/json?address=" + urllib.quote(address) + "&key=AIzaSyByadV-fst2KLQvu9AdiRcZAetWGwXlG9Q"
			geoResp = requests.get(geoReq)
			jgeo = geoResp.json()
			if geoResp.status_code == 200 and jgeo['status'] == 'OK':
				lat = jgeo['results'][0]['geometry']['location']['lat']
				lng = jgeo['results'][0]['geometry']['location']['lng']
				area = str(lat) + " " + str(lng)
			else:
				area = address.split(',')[-2].strip() 
		else:
			area = "na"
		
		idA = links[i].split("/")[2]
		
		p = p.strip().replace("\"",""); 
		apts[i] = ( str(idA).encode('utf-8'), p.strip().replace(",", "").encode('utf-8'), str(price).encode('utf-8'), str(meters).encode('utf-8'), str(rooms).encode('utf-8'), address, area,  host + links[i] )
		 
		# print(str(i+1) + "] " + p.strip() + ".\n Details: "+ details[i].strip() + "\n")
	
		#print(str(i) + ") " + apts[i]["title"] + ".\nDetails: " + apts[i]["price"] + ", " + apts[i]["meters"] + ", " + apts[i]["rooms"] )
		#print( apts[i] )
		
		print( "\"" + apts[i][0] + "\"," + "\"" + apts[i][1] + "\"," + "\"" + apts[i][2] + "\"," + "\"" + apts[i][3] + "\"," + "\"" + apts[i][4] + "\"," + "\"" + apts[i][5] + "\"," + "\"" + apts[i][6] + "\"," + "\"" + apts[i][7] + "\"" )
		#debug
		#print("meters: " + str( meters.__len__() ))
		#print ( "Meters: " + str(details[(i*4)+1].strip().encode('utf-8')) + ". Size: " + str(details[(i*4)+1].strip().__len__()) )
		#print(  details[i*4].encode('utf-8').strip() + details[(i*4) + 1].encode('utf-8').strip() + details[(i*4) + 2].encode('utf-8').strip() )
		
		
		i += 1

	#print("\n\n Search results: " + numOfResults[0] + ". Page results: " + str(i))


