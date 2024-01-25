
import os
import random
from flask import Flask, jsonify, request, send_file, send_from_directory, session
from PIL import Image
from random import randrange
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

#initialisation du jeu : sélection de 1024 images

@app.route('/image/init/', methods=['POST'])

def init_game():
    data = request.json
    gamemod = data["gamemod"]
    nb_upload = data["nb_upload"]

    list_image = []


    nb_images_bdd = 40000

    if gamemod == 1: #aminoguess
        grid_size = 1024
    elif gamemod == 2: #ariane and theseus
        grid_size = 24


    while len(list_image) < grid_size-nb_upload:

        r = randrange(0, nb_images_bdd) + 52000 #the number of the images start at 52000
        if r not in list_image:
            list_image.append(r)

    # envoie liste d'id images
    return jsonify(list_image=list_image)

@app.route('/image/upload/', methods=['POST'])
def upload_img():
    random_name = random.randint(1, 50000)
    file = request.files['image']
    image_data = file.read()    
    image = Image.open(io.BytesIO(image_data))

    target_width = 178
    target_height = 218
    resized_image = resize_and_crop_image(image, target_width, target_height)


    folder_name = "temp"
    folder_path = os.path.join(os.getcwd(), folder_name)

    # add mkdir if not exist
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    resized_image.save(os.path.join(folder_path, f"{random_name}.jpg"))

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