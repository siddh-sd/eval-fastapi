from uuid import UUID, uuid4
from fastapi import UploadFile
from azure.storage.blob import BlobServiceClient, ContentSettings
from config import AZURE_STORAGE_ACCOUNT_NAME,AZURE_STORAGE_ACCOUNT_KEY,AZURE_CONTAINER_NAME
from pydantic import BaseModel

# Configure Azure Storage Blob
blob_service_client = BlobServiceClient.from_connection_string(
    f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT_NAME};AccountKey={AZURE_STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)


class Details(BaseModel):
  id: UUID
  name: str


async def save_file_to_azure(file: UploadFile):
  try:
    unique_blob_name = f"{uuid4()}-{file.filename}"
    blob_client = container_client.get_blob_client(unique_blob_name)
    content = file.file.read()

    blob_client.upload_blob(content, content_settings=ContentSettings(content_type=file.content_type))

    return f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{unique_blob_name}"
  except Exception as e:
    raise e
  

async def delete_file_from_azure(file_url: str):
  try:
    blob_name = file_url.split('/')[-1]
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.delete_blob()
  except Exception as e:
    raise e