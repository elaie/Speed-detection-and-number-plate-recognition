import cv2
import easyocr
import numpy as np
from matplotlib import pyplot as plt
import time

from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()
from ultralytics import YOLO
from IPython.display import display, Image

# load an pretrained model
model = YOLO('best.pt') 
model.conf = 0.4  #confidence threshold for detection

#initializing ocr
reader = easyocr.Reader(['en', 'ne'])

def recognize_number_plate(image):
    vehicle_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB
    # Perform object detection using YOLO
    detections = model(vehicle_image)
    
    # Extract bounding boxes and crop number plate regions
    number_plate_box = None
    for detection in detections[0].boxes.data:
        if detection[5] == 0:
            number_plate_box = detection[:4]
            break
    
    # Crop the number plate region
    if number_plate_box is not None:
        x1, y1, x2, y2 = number_plate_box
        cropped_image = vehicle_image[int(y1):int(y2), int(x1):int(x2)]
    else:
        print("Number plate not found.")
    
    # Perform OCR on the number plate image
    recognized_plates = []
    result = reader.readtext(cropped_image)
    # Extract the text from the OCR result
    if result:
        recognized_plate = result[0][1]
        recognized_plates.append(recognized_plate)
    
    return recognized_plates

# Open the video stream
cap = cv2.VideoCapture('your_streaming_video_url')

while cap.isOpened():
    # Read a frame from the video stream
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Pass the frame to the recognition function
    recognized_plates = recognize_number_plate(frame)

    # Print the recognized number plates
    for plate in recognized_plates:
        print(plate)

    # Display the frame
    cv2.imshow('Video Stream', frame)
    
    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close windows
cap.release()
cv2.destroyAllWindows()

