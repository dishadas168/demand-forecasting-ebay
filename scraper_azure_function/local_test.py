from unittest.mock import patch, ANY
import azure.functions as func
from function_app import scrape_ebay_fns
from utils.scrape_ebay import scrape_ebay_and_store

url = "http://localhost:7071/api/scrape_ebay_fns"

def test_hello_world():

    req = func.HttpRequest(
        method="POST",
        body={
            "scrape_date":"Sold  Nov 5, 2023",
            "country":"China",
            "tea_type":"Pu-erh"
        },
        url=url
    )

    # Call the function.
    func_call = scrape_ebay_fns.build().get_user_function()
    response = func_call(req)
    print(response.get_body())
    assert response.status_code == 200

test_hello_world()


    