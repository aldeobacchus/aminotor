
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient ,generate_blob_sas, BlobSasPermissions

from flask import jsonify
from random import randrange
import random
from flask import Flask, jsonify, request, send_file, send_from_directory, session
from PIL import Image
from random import randrange
from flask_cors import CORS
import io
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

connection_string = "DefaultEndpointsProtocol=https;AccountName=aminotorimages;AccountKey=le1LEtQNTWr3JeEO7p3df7XwiQ8kU5tEFc6+Qh8cnBmGAEDYXbVE+RnG6+cjZpfDLA26E7t+DThs+ASt8U5seQ==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client('images')




def generate_sas_url(blob_service_client, container_name, blob_name):
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
    )
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

    return blob_url


@app.route('/image/init/', methods=['POST'])
def init_game():
    data = request.json
    gamemod = data["gamemod"]
    list_upload = data["list_upload"]
    nb_upload = len(list_upload)

    list_image = []


    nb_images_bdd = 40000

    if gamemod == 1: #aminoguess
        grid_size = 16
    elif gamemod == 2: #ariane and theseus
        grid_size = 24

    container_name = 'images'

    for i in range(grid_size):
        if i < nb_upload:
            value = list_upload[i]
        else :
            value = randrange(0, nb_images_bdd) + 52000
        blob_name = f"{value:06}.jpg"
        blob_client = container_client.get_blob_client(blob_name)
        if blob_client.exists() and blob_name not in list_image:
            list_image.append(blob_name)
 
    # Fetch URLs of the blobs
    image_urls = []
    for image in list_image:
        
        sas_url = generate_sas_url(blob_service_client, container_name, image)
        image_urls.append(sas_url)

        #if r not in list_image:
        #    list_image.append(r)

    # envoie liste d'id images
    return jsonify(list_image=list_image , image_urls=image_urls)

@app.route('/image/upload/', methods=['POST'])
def upload_img():
    random_name = random.randint(1, 50000)
    file = request.files['image']
    image_data = file.read()    
    image = Image.open(io.BytesIO(image_data))

    target_width = 178
    target_height = 218
    resized_image = resize_and_crop_image(image, target_width, target_height)


    # Convert the processed image to bytes
    img_byte_arr = io.BytesIO()
    resized_image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    # Upload the image to Azure Blob Storage
    blob_name = f"{random_name:05}.jpg"

    container_name = 'images'
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    blob_client.upload_blob(img_byte_arr, blob_type="BlockBlob")
    
    # access to the image
    sas_url = generate_sas_url(blob_service_client, container_name, blob_name)
    print(sas_url)

    return jsonify(
        random_name=random_name
    )

def resize_and_crop_image(image, target_width, target_height):

    original_width, original_height = image.size

    width_ratio = target_width / original_width
    height_ratio = target_height / original_height

    resize_ratio = max(width_ratio, height_ratio)

    new_width = int(original_width * resize_ratio)
    new_height = int(original_height * resize_ratio)
    resized_image = image.resize((new_width, new_height),
                                 Image.ANTIALIAS if "ANTIALIAS" in dir(Image) else Image.BILINEAR)

    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2

    cropped_image = resized_image.crop((left, top, right, bottom))

    return cropped_image

@app.route('/image/delete/', methods=['POST'])
def delete_img():
    
    data = request.json

    list_upload = data["list_upload"]
    
    folder_name = "temp"
    folder_path = os.path.join(os.getcwd(), folder_name)

    for image_id in list_upload:
        file_path = os.path.join(folder_path, f"{image_id}.jpg")
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify(
        success=True
    )


@app.route('/image/get/<int:img>', methods=['GET'])
def get_img(img):
    img_name = f"{img}.jpg"
    folder_name = "temp"
    folder_path = os.path.join(os.getcwd(), folder_name)  
    img_path = os.path.join(folder_path, img_name)  
    return send_file(img_path, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True, port = 5001)