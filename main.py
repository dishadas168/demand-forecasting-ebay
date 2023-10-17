from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests

page=1
while page:
    print("Page :",page)
    # Update the link of the item
    link = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone&LH_Sold=1&_oac=1&_pgn={page}"

    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'html.parser')
        if soup.find('div', attrs={'class':'s-error'}):
            page=0
        items = soup.find_all('li',attrs={'class':'s-item s-item__pl-on-bottom'})

    print("Count :", len(items))
    # for item in items:
        
    #     try:
    #         print("Name : ", item.find('span', attrs={'role':'heading'}).text)
    #         print("Date sold : ", item.find('div', attrs={'class':'s-item__caption-section'}).find('span', attrs={'class':'POSITIVE'}).text)
    #         print("Price : ", item.find('span', attrs={'class':'s-item__price'} ).text)
    #     except:
    #         None

    #     try:
    #         print("Bids :", item.find('span', attrs={'class':'s-item__bids s-item__bidCount'}).text)
    #     except:
    #         None
    #     try:
    #         print("Purchase Option : ", item.find('span', attrs={'class':'s-item__purchase-options s-item__purchaseOptions'}).text)
    #     except:
    #         None

    #     print("\n")
    page += 1
