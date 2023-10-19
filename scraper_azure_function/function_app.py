import azure.functions as func
import logging
from utils.scrape_ebay import scrape_ebay_and_store

app = func.FunctionApp()

@app.route(route="scrape_ebay_fns", auth_level=func.AuthLevel.ANONYMOUS)
def scrape_ebay_fns(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    scrape_ebay_and_store()

    return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
            status_code=200
    )