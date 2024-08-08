from ultralytics import YOLO
import os
import requests
import json
from PIL import Image
from io import BytesIO
import pandas as pd

def Inference(image_path):
    model = YOLO("classify/train/weights/best.pt")
    results = model.predict(image_path, show=False, save=False, save_txt=False)
    id = results[0].probs.top1
    clsName = results[0].names[id]
    return clsName

def patch_api_data(image_id, author_id, labels):
    url = f"https://api.floodwatch-ai.com/photos/{image_id}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "labels": labels,
        "authorId": author_id
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response

def save_image_from_url(url, file_path):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(file_path)

def update_csv(image_id, label, csv_file='image_labels.csv'):
    # Check if the CSV file exists
    if os.path.exists(csv_file):
        # Read the existing data
        df = pd.read_csv(csv_file)
    else:
        # Create a new dataframe if the file does not exist
        df = pd.DataFrame(columns=['image_id', 'label','checker'])
    
    # Check if the image_id already exists in the dataframe
    if image_id not in df['image_id'].values:
        # Append new data
        new_data = pd.DataFrame([[image_id, label]], columns=['image_id', 'label'])
        df = pd.concat([df, new_data], ignore_index=True)
        # Save the updated dataframe to the CSV file
        df.to_csv(csv_file, index=False)
        print(f"Added image_id {image_id} with label {label} to {csv_file}")
    else:
        print(f"image_id {image_id} already exists in {csv_file}")

while True:
    floodwatch_api = "https://api.floodwatch-ai.com/photos/next/12"
    photos_response = requests.get(floodwatch_api)
    photos_data = photos_response.json()
    image_id = photos_data.get("id")
    image_url = photos_data.get("dataUrl")

    save_image_from_url(image_url, "test.jpg")
    print(f"Saved image {image_id} from {image_url} to test.jpg")

    inference_result = Inference("test.jpg")
    print(inference_result)

    author_id = 12
    labels = [
        {"labelNames": [inference_result], "taskName": "road_condition"},
    ]

    response = patch_api_data(image_id, author_id, labels)
    print(response.text)

    # Update the CSV file with the image_id and label
    update_csv(image_id, inference_result)
