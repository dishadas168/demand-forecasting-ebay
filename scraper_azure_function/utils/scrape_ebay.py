from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import urllib.parse
from datetime import datetime
import hashlib
from base64 import b64encode
import pymongo
import calendar
from dateutil import tz

mongodb_uri="mongodb://ebay-storage-db:Z07RYTm2ZOMWBNeioffbKYDQ7Vgm4IfspqOX8SMk7TT0vDgnOadG1GelNUaeRBAvCIL5CjOM7zm8ACDbZGMfpQ==@ebay-storage-db.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@ebay-storage-db@"

client = pymongo.MongoClient(mongodb_uri)
db = client["demand-froecasting-ebay"]
raw_collection = db["raw"]

def make_uid(*args):
  uid = ""
  for arg in args:
    uid = uid + arg
  uid = b64encode(uid.encode('ascii'))
  return hashlib.sha256(uid).hexdigest()

def encode_hyphen(string):
    return string.replace("-", "%252D")

def get_scrape_date(date_string):

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Chicago')
    date_string = date_string.split(".")[0]
    date_format = "%Y-%m-%dT%H:%M:%S"
    dt_obj = datetime.strptime(date_string, date_format)
    dt_obj = dt_obj.replace(tzinfo=from_zone)
    dt_obj = dt_obj.astimezone(to_zone)
    month = calendar.month_abbr[int(dt_obj.month)]

    scrape_date = f"Sold  {month} {dt_obj.day}, {dt_obj.year}"
    return scrape_date

def scrape_ebay_and_store(country, tea_type, scrape_date):

  if len(scrape_date) > 0:
    scrape_date = get_scrape_date(scrape_date)

  page=1
  item_count = 0
  while item_count< 10000 :

      country_encoded = urllib.parse.quote(urllib.parse.quote(country, safe=''), safe='') if country!= "Not Specified" else "!"
      tea_type_encoded= urllib.parse.quote(urllib.parse.quote(tea_type, safe=''), safe='') if tea_type!= "Not Specified" else "!"
      tea_type_encoded = encode_hyphen(tea_type_encoded)
      link = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=tea&_sacat=0&LH_ItemCondition=1000&LH_BIN=1&LH_Sold=1&LH_Complete=1&Country%252FRegion%2520of%2520Manufacture={country_encoded}&rt=nc&Type={tea_type_encoded}&_dcat=38181&_pgn={page}"

      req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
      webpage = urlopen(req).read()

      with requests.Session() as c:
          soup = BeautifulSoup(webpage, 'html.parser')
          items = soup.find_all('li',attrs={'class':'s-item s-item__pl-on-bottom'})

      data = []

      for item in items:
          item_data = {}

          if item.attrs["id"] == "":
            continue

          try:
              item_data["date_sold"] = item.find('div', attrs={'class':'s-item__caption-section'}).find('span', attrs={'class':'POSITIVE'}).text
              if len(scrape_date) > 0 and item_data["date_sold"] != scrape_date:
                  continue
              item_data["title"] = item.find('span', attrs={'role':'heading'}).text
              item_data['subtitle'] = item.find('div', attrs={'class':'s-item__subtitle'}).find('span', attrs={'class':'SECONDARY_INFO'}).text
              item_data["seller"] = item.find('span', attrs={'class':'s-item__seller-info-text'}).text
          except Exception as e:
              None

          try:

              price_list = item.find('span', attrs={'class':'s-item__price'})
              price_text=""
              for price in price_list.find_all('span'):
                  price_text = price_text + price.text
              item_data["price"] = price_text

              item_data["_id"] = make_uid(country, tea_type, item_data["title"],item_data['subtitle'],item_data["price"],item_data["date_sold"],item_data["seller"])
          except Exception as e:
              None

          try:
              item_data["country"] = country
              item_data["tea_type"] = tea_type
              item_data["url"] = item.find('a', attrs={'class': 's-item__link'}).attrs["href"]

          except Exception as e:
              None

          try:
              item_data["purchase_option"] = item.find('span', attrs={'class':'s-item__purchase-options s-item__purchaseOptions'}).text
          except:
              None
          try:
              item_data["shipping"] = item.find('span', attrs={'class':'s-item__shipping s-item__logisticsCost'}).text
          except:
              None
          try:
              item_data["location"] = item.find('span', attrs={'class':'s-item__location s-item__itemLocation'}).text
          except:
              None
          item_data["date_extracted"] = datetime.now()

          item_data["page"] = page
          item_data["scraped"] = False
          data.append(item_data)

      item_count += len(data)

      if len(data) == 0:
        break

      try:
        raw_collection.insert_many(data)
      except Exception as e:
        None

      #If page exists, continue, else break
      pages = soup.find_all('div',attrs={'class':'s-pagination'})
      page_items = pages[0].find_all('a', attrs={'class':'pagination__item'})
      if len(page_items) and any([item.text == str(page+1) for item in page_items]):
        page += 1
      else:
        break

  return data
