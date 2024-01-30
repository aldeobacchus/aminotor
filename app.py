from azure.storage.blob import BlobServiceClient,generate_blob_sas, BlobSasPermissions, ContentSettings

from flask import jsonify
from random import randrange
import random
from flask import Flask, jsonify, request
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
container_name = 'images'

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

@app.route('/')
def hello():
    return 'Bienvenue chez InitImageService'

@app.route('/image/init/', methods=['POST'])
def init_game():
    data = request.json
    gamemod = data["gamemod"]
    list_upload = data["list_upload"]
    nb_upload = len(list_upload)
    print(nb_upload)

    list_image = []
    list_blob = []

    nb_images_bdd = 40000

    if gamemod == 1: #aminoguess
        grid_size = 128
    elif gamemod == 2: #ariane and theseus
        grid_size = 24

    for i in range(grid_size):
        if i < nb_upload:
            value = list_upload[i]
            print(value)
        else :
            value = randrange(0, nb_images_bdd) + 50000
        blob_name = f"{value:06}.jpg"
        blob_client = container_client.get_blob_client(blob_name)
        if blob_client.exists():
            list_image.append(value)
            list_blob.append(blob_name)
            
    # Fetch URLs of the blobs
    image_urls = []
    for blob in list_blob:
        
        sas_url = generate_sas_url(blob_service_client, container_name, blob)
        image_urls.append(sas_url)

    print(image_urls[0])
    # envoie liste d'id images
    return jsonify(list_image=list_image , image_urls=image_urls)

@app.route('/image/upload/', methods=['POST'])
def upload_img():
    random_name = random.randint(1, 2000)
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

    content_settings = ContentSettings(content_type='image/jpeg')
    
    # Upload the image to Azure Blob Storage
    blob_name = f"{random_name:06}.jpg" 

    container_name = 'images'
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    blob_client.upload_blob(img_byte_arr, blob_type="BlockBlob", content_settings=content_settings)
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
    print(list_upload)

    for image_id in list_upload:
        blob_name = f"{image_id:06}.jpg"
        container_client.delete_blob(blob_name)
    
    return jsonify(
        success=True
    )

if __name__ == '__main__':
    app.run(debug=True, port = 5001)