import os
from azure.storage.blob import BlobServiceClient

class AzureBlobUploader:
    def __init__(self, container_name, account_name, account_key):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};EndpointSuffix=core.windows.net"
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def upload_file(self, local_file_path, blob_name=None):
        if blob_name is None:
            blob_name = os.path.basename(local_file_path)
        
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)

        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data)
        
        print(f"Uploaded {blob_name}.")

    def upload_folder(self, local_folder_path, remote_folder_path=''):
        for root, _, files in os.walk(local_folder_path):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                remote_file_path = os.path.join(remote_folder_path, file_name)
                self.upload_file(local_file_path, remote_file_path)

    def upload_selected_files(self, file_paths):
        for local_file_path, blob_name in file_paths:
            self.upload_file(local_file_path, blob_name)

# Azure Storage account details
account_name = 'dummypush'
account_key = 'UaTWFz7Kx6pL8Hu222QBae9UiG20WLg7BHkBFBXEq6GmfjHZ8Ev+Qj0I9tKqCKxMTz5jWqFFDFAA+AStmsPOtQ=='
container_name = 'haritestpush'

# Create an instance of AzureBlobUploader
uploader = AzureBlobUploader(container_name, account_name, account_key)

# Upload a single file
local_file_path = 'D:/Unislink intern works/azure storage push project/hello.txt'
uploader.upload_file(local_file_path)

# Upload a folder
local_folder_path = 'D:/Unislink intern works/azure storage push project/folder'
uploader.upload_folder(local_folder_path)

# Upload selected files
file_paths = [
    ('D:/Unislink intern works/azure storage push project/file1.txt'),
    ('D:/Unislink intern works/azure storage push project/file2.txt', 'custom_blob_name.txt'),
    ('D:/Unislink intern works/azure storage push project/file3.txt')
]
uploader.upload_selected_files(file_paths)
