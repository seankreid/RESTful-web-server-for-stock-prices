- Responds to GET requests to an endpoint of "price" with a query string parameter of "stock" and then will use BeautifulSoup to do a live lookup of that stock on MarketWatch and will return a textual response containing just the current price of the stock

- Responds to GET requests to an endpoint of "name" with a query string parameter of "stock" and then uses  "sqlite3" module to read the data of stock abbreviations to names and will return the company name based on the stock abbreviation passed in the URL 

- Responds to GET requests to an endpoint of "addStock" with two query string URL parameters "name", and "abbreviation" that will add the requested company name and abbreviation to the SQLite3 database and return a "success" message if it is added or en "exists" error message if the stock was already present
