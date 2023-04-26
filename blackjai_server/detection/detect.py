import cv2 as cv


# Function to detect card type and save the prediction to a buffer image
def detect_card_type(image, model):
    # infer based on frame from webcam and save the prediction
    json_data = model.predict(image, confidence=80, overlap=30).json()

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
