import cv2 as cv
from ultralytics import YOLO


# Function to detect card type and save the prediction to a buffer image
def detect_card_type_roboflow(image, model):
    # infer based on frame from webcam and save the prediction
    json_data = model.predict(image, confidence=85, overlap=30).json()

    # check if json contains any predictions and show the prediction if it does
    if json_data["predictions"]:
        # print(str(len(json_data["predictions"])) + " prediction(s):")

        for prediction in json_data["predictions"]:
            # get the bounding box of the prediction
            x1 = int(prediction["x"])
            y1 = int(prediction["y"])
            x2 = int(x1 + prediction["width"])
            y2 = int(y1 + prediction["height"])

            # get prediction info
            card_type = prediction["class"]
            confidence = prediction["confidence"]
            # print(str(card_type) + " (" + str(round(100 * confidence, 3)) + "%)")

            # draw the bounding box and label on the image
            cv.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv.putText(image, card_type, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # print()
    return image, json_data

def detect_card_type_yolo(image, model):
    # Get results from yolo prediction
    results = model.predict(image, conf=0.5, verbose=False)
    num_detections = len(results[0].boxes.xyxy)

    boxes = results[0].boxes
    json_data = {}
    if num_detections > 0:
        json_data["predictions"] = []
    for i in range(len(results[0].boxes.xyxy)):
        curr_prediction = {}
        curr_prediction["class"] = results[0].names[boxes.cls[i].item()]

        x1 = int(boxes.xyxy[i][0].item())
        y1 = int(boxes.xyxy[i][1].item())
        x2 = int(boxes.xyxy[i][2].item())
        y2 = int(boxes.xyxy[i][3].item())

        curr_prediction["x"] = x1
        curr_prediction["y"] = y1
        curr_prediction["width"] = x2 - x1
        curr_prediction["height"] = y2 - y1

        curr_prediction["confidence"] = round(boxes.conf[i].item(), 3)

        json_data["predictions"].append(curr_prediction)

    # plot the bounding boxes and labels on the image
    annotated_image = results[0].plot()

    return annotated_image, json_data
