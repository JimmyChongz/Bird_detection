# Migratory Bird Detection and Counting

This project is a web application developed using **Flask** to detect and count migratory birds using the **YOLOv7** model. The application allows users to upload images or MP4 videos, and the server will run the YOLOv7 detection function to identify and count the number of birds in the uploaded media.

## Features
- **Bird Detection**: Detect and count migratory birds in images or videos using YOLOv7.
- **Web Interface**: Built with Flask, allowing users to easily upload pictures or MP4 videos for detection.
- **Trained on 7,000+ Images**: The model is trained on a dataset of over 7,000 images of migratory birds for improved accuracy.

## Installation

### Prerequisites
Ensure you have Python 3.7+ installed, and install the following dependencies:

```bash
pip install -r requirements.txt
```
Then, run the following command to start the project.
```bash
flask run
```
This project will be deployed on your `localhost:5000` .

