import azure.functions as func
import logging
from utils.scrape_ebay import scrape_ebay_and_store
import json

app = func.FunctionApp()

@app.route(route="scrape_ebay_fns", auth_level=func.AuthLevel.ANONYMOUS)
def scrape_ebay_fns(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request. Sent raw scraped records to CosmosDB.')
    
    body = req.get_body().decode('utf-8')
    body=json.loads(body)

    scrape_date =  body['scrape_date']
    country = body['country']
    tea_type = body['tea_type']

    if scrape_date and country and tea_type: 

        scrape_ebay_and_store(scrape_date, country, tea_type)
        return func.HttpResponse( 
            f"This HTTP-triggered function " 
            f"executed successfully for date {scrape_date}, country {country} and tea type {tea_type}") 
    else: 
        return func.HttpResponse( 
            "This HTTP-triggered function executed successfully. " 
            "Pass scrape_date, country and tea type data in the query string or in the request body for a" 
            " personalized response.", 
            status_code=200 
        ) 