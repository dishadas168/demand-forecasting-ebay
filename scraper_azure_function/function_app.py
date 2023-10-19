import azure.functions as func
import logging
from utils.send_data import upload_to_blob_storage
from utils.scrape_ebay import scrape_ebay_and_store
import os

app = func.FunctionApp()

@app.route(route="scrape_ebay_fns", auth_level=func.AuthLevel.ANONYMOUS)
def scrape_ebay_fns(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    outfile = "jsonout.jsonl"
    scrape_ebay_and_store()
    # upload_to_blob_storage(outfile, outfile)
    # os.remove(outfile)

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )