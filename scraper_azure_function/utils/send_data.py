from azure.storage.blob import BlobServiceClient

storage_account_key = "KcA0iCikjJSqSRqG3WYqW9lpyB7MTy9yKqm0vRHyfYss33Vjj3BTss5tXOOgFCwF7QZ3w8O3DRE3+AStbiTPLQ=="
storage_account_name = "demandforecastingebaysa"
connection_string = "DefaultEndpointsProtocol=https;AccountName=demandforecastingebaysa;AccountKey=KcA0iCikjJSqSRqG3WYqW9lpyB7MTy9yKqm0vRHyfYss33Vjj3BTss5tXOOgFCwF7QZ3w8O3DRE3+AStbiTPLQ==;EndpointSuffix=core.windows.net"
container_name = "raw"

def upload_blob_stream(input, filename):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.upload_blob(input, blob_type="BlockBlob", overwrite=True)