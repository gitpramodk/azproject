from flask import Flask, request, redirect, render_template 

import os   
from azure.storage.blob import BlobServiceClient
import configparser

app = Flask(__name__) 

config = configparser.ConfigParser()
config.read("config.py")

# Account Connection String
connect_str = config['DEFAULT']['connect_str']
# Container name
container_name = config['DEFAULT'] ['container_name']

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account

try:
    container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored
    container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
except Exception as e:
    container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist


#flask endpoint for Home page of upload
@app.route("/") 
def main():  
    return render_template('index.html')

#flask endpoint to upload a photo  
@app.route("/upload", methods=["POST"])  
def process_upload():  
    filenames = ""  
    for file in request.files.getlist("photos"):
        try:
            container_client.upload_blob(file.filename, file) # upload the file to the container using the filename as the blob name
            filenames += file.filename + "<br /> "
        except Exception as e:
            print(e)
            print("Ignoring duplicate filenames") # ignore duplicate filenames


    return render_template('upload.html') 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


