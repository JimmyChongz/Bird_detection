# Migratory Bird Detection and Counting

This project is a web application developed using **Flask** to detect and count migratory birds using the **YOLOv7** model. The application allows users to upload images or MP4 videos, and the server will run the YOLOv7 detection function to identify and count the number of birds in the uploaded media.

## Features
- **Bird Detection**: Detect and count migratory birds in images or videos using YOLOv7.
- **Web Interface**: Built with Flask, allowing users to easily upload pictures or MP4 videos for detection.
- **Trained on 7,000+ Images**: The model is trained on a dataset of over 7,000 images of migratory birds for improved accuracy.

## Build environment
```bash
conda create -n yolov7 python=3.11
conda activate yolov7
cd yolov7
pip install -r requirements.txt
pip install torch==2.5.1 torchvision==0.20.1+cu124 --index-url https://download.pytorch.org/whl/cu124
```
Then, run the following command to start the project.
```bash
flask run
```
This project will be deployed on your `localhost:5000` .
