from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import json
import jsonlines

page=1
while page < 6:
    print("Page :",page)
    # Update the link of the item
    link = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone&LH_Sold=1&_oac=1&_pgn={page}"

    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'html.parser')
        # if soup.find('div', attrs={'class':'s-error'}):
        #     break
        items = soup.find_all('li',attrs={'class':'s-item s-item__pl-on-bottom'})

    data = []
    print("Count :", len(items))
    for item in items:
        item_data = {}
        try:
            item_data["name"] = item.find('span', attrs={'role':'heading'}).text
            item_data["date_sold"] = item.find('div', attrs={'class':'s-item__caption-section'}).find('span', attrs={'class':'POSITIVE'}).text
            item_data["price"] = item.find('span', attrs={'class':'s-item__price'} ).text
            # print("Name : ", item.find('span', attrs={'role':'heading'}).text)
            # print("Date sold : ", item.find('div', attrs={'class':'s-item__caption-section'}).find('span', attrs={'class':'POSITIVE'}).text)
            # print("Price : ", item.find('span', attrs={'class':'s-item__price'} ).text)
        except:
            None

        try:
            item_data["bids"] = item.find('span', attrs={'class':'s-item__bids s-item__bidCount'}).text
            # print("Bids :", item.find('span', attrs={'class':'s-item__bids s-item__bidCount'}).text)
        except:
            None
        try:
            item_data["purchase_option"] = item.find('span', attrs={'class':'s-item__purchase-options s-item__purchaseOptions'}).text
            # print("Purchase Option : ", item.find('span', attrs={'class':'s-item__purchase-options s-item__purchaseOptions'}).text)
        except:
            None
        item_data["page"] = page
        data.append(item_data)
        print("\n")
    
    # final = json.dump(data)
    # with open(f"mydata_{page}.json", "w") as final:
    #     json.dump(data, final)
    with jsonlines.open('jsonout.jsonl', mode='a') as writer:
        writer.write(data)

    page += 1

