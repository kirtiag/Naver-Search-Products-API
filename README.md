NAVER SHOPPING SCRAPER API
============================================================

📌 DESCRIPTION:
------------------------------------------------------------
This is a Flask-based REST API that scrapes product listings
from Naver Shopping using pagination and proxy rotation.
It supports retry-once logic for HTTP 418 errors and logs
average latency per request.

The script allows requesting up to 1000 products at once
with a target average latency of ≤ 6 seconds per request.

------------------------------------------------------------
🧱 REQUIREMENTS:
------------------------------------------------------------
Install the required Python libraries using:

    pip install Flask requests fake_useragent(I used try except to handle this)

------------------------------------------------------------
⚙️ CONFIGURATION:
------------------------------------------------------------
Create Crentials.py:

usename = "proxyusername" 
password = "proxypasswrd"

please change your Crentials in this script.

- Proxy: Proxy Empire rotating proxy is used by default.
- Fake User-Agent: Generated per request using fake_useragent.

------------------------------------------------------------
🚀 HOW TO RUN:
------------------------------------------------------------

Run the script using:

    python main.py

Flask will start the API server at:

     http://127.0.0.1:5000

Use ngrok to expose the local API:

ngrok http 5000	 

Forwarding                    https://macaque-sacred-sadly.ngrok-free.app -> http://localhost:5000  

Now your API is publicly accessible like:

https://macaque-sacred-sadly.ngrok-free.app/naver?query_url=your_url

Example:

https://macaque-sacred-sadly.ngrok-free.app/naver?query_url=https://search.shopping.naver.com/ns/v1/search/paged-composite-cards?cursor=1&pageSize=1000&query=iphone&searchMethod=all.basic&isFreshCategory=false&isOriginalQuerySearch=false&isCatalogDiversifyOff=true&categoryIdsForPromotions=50000204&hiddenNonProductCard=false&duplicatedNvMids=88368494386&duplicatedNvMids=89015751596&hasMoreAd=true
------------------------------------------------------------
🌐 API USAGE:
------------------------------------------------------------

GET Endpoint:
    /naver?query_url=your_url

Example:
curl "http://127.0.0.1:5000/naver?query_url=https://search.shopping.naver.com/ns/v1/search/paged-composite-cards?cursor=1&pageSize=1000&query=iphone&searchMethod=all.basic&isFreshCategory=false&isOriginalQuerySearch=false&isCatalogDiversifyOff=true&categoryIdsForPromotions=50000204&hiddenNonProductCard=false&duplicatedNvMids=88368494386&duplicatedNvMids=89015751596&hasMoreAd=true"  

Query Parameters:
    - query_url (required): Full Naver API URL to scrape from
	
   - pageSize Max Value: 1000
   - The server paginates internally by 100 products per request.

⚠️ Limitations:
- The server limits the maximum products scraped per call to **1000**.
- To fetch the **next 1000 products**, update the `cursor` parameter in the `query_url` accordingly.
  Example:
    - First call: `cursor=1`
    - Second call: `cursor=1001`
    - Third call: `cursor=2001`
  and so on...

    

------------------------------------------------------------
🧾 RESPONSE FORMAT:
------------------------------------------------------------
Success (HTTP 200):
{
    "total": 100,
    "products": [
        {
            "product_name": "iPhone 14 Pro",
            "price": 1350000,
            "product_url": "https://product.naver.com/item/..."
        },
        ...
    ]
}




if want all other informatiuon then I can take,this is only for example.

Failure (HTTP 500 or 400):
{
    "error": "Failed to retrieve data"
}

------------------------------------------------------------
📊 LATENCY LOGGING:
------------------------------------------------------------
For every request batch:
- Average latency per page is printed in the server log.

Example:
✅ Average latency per page: 4.88 seconds

