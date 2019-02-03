#!/usr/bin/env python3

# Sean Reid

from http.server import BaseHTTPRequestHandler, HTTPServer
from bs4 import BeautifulSoup
import urllib.parse as urlparse
import requests
import time
import sqlite3

conn = sqlite3.connect('stocks.db')
c = conn.cursor()
c.execute(               				 #create a table if one does not exist
	'''CREATE TABLE IF NOT EXISTS STOCKS
		( NAME TEXT PRIMARY KEY, \
		  ABREVIATION TEXT \
		  )''' 
		)
conn.commit() 

def main():
	
	PORT = 8880
	httpd = HTTPServer(('127.0.0.1', PORT), MyHTTPServer)
	print("serving at port", PORT)
	httpd.serve_forever()

class MyHTTPServer(BaseHTTPRequestHandler):
	def do_GET(self):
     
		parsed = urlparse.urlparse(self.path)
		parameters = urlparse.parse_qs(parsed.query)
		#stock = parameters['stock'][0].lower()
		#name = parameters['name'][0].lower()
   
		if(parsed.path == '/price'): 
			stock = parameters['stock'][0].lower()
			page = requests.get("https://www.marketwatch.com/investing/stock/" + stock)
			soup = BeautifulSoup(page.text, "html.parser")
			price = soup.find("bg-quote", {"field":"Last"}).contents[0]


			self.send_response(200)
			self.send_header('Content-Type',
							 'text/plain; charset=utf-8')
			self.end_headers()
			self.wfile.write(price.encode('utf-8'))

		elif(parsed.path == '/name'):
			conn = sqlite3.connect('stocks.db')
			c = conn.cursor()
			try: 
				c.execute(' SELECT * FROM Stocks WHERE abreviation = ' + name)
				abrv = c.fetchone()
				self.wfile.write(abrv.encode('utf-8'))
			except:
				self.wfile.write("Error! That stock does not exist!.".encode('utf-8'))

		elif(parsed.path == '/addName'):
			name = parameters['name'][0].lower()
			conn = sqlite3.connect('stocks.db')
			c = conn.cursor()
			try:
				c.execute("INSERT INTO Stocks (name, abreviation) VALUES(" + name + ", '" + abreviation + "')");
				conn.commit()
				self.wfile.write("Stock was successfully added.".encode('utf-8'))
			except:
				self.wfile.write("That stock already exists.")


if __name__ == '__main__':
	main()

conn.close()
