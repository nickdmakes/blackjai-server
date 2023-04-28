import sys
import os
import traceback
import cv2 as cv
import imagezmq
import threading
import numpy as np
from roboflow import Roboflow
from time import sleep
import datetime
from PIL import Image
from ultralytics import YOLO
from blackjai_server.detection.detect import detect_card_type_roboflow, detect_card_type_yolo
from blackjai_server.engine.engine import BlackJAIEngine
from blackjai_server.preprocessing.preprocess import greyscale, apply_contrast, apply_threshold, convert_to_rgb, apply_dilate


"""
BlackJAIServer:
This class is used to start the server and receive images from the publisher.
"""
class BlackJAIServer:
    def __init__(self, hostname="127.0.0.1", port=5555, view_mode="view"):
        self.hostname = hostname
        self.port = port
        self.view_mode = view_mode

        # Load in YOLO model
        self.yolo_model = YOLO(f"{os.getcwd()}/blackjai_server/ml_models/best_m_31eps_all.pt")

    def start(self):
        receiver = VideoStreamSubscriber(self.hostname, self.port)
        engine = BlackJAIEngine(frame_size=(1920, 1080), buffer_size=6)

        try:
            if self.view_mode == "view":
                while True:
                    # Receive image from publisher
                    msg, frame = receiver.receive(timeout=2)

                    # Display image
                    image = cv.imdecode(np.frombuffer(frame, dtype='uint8'), -1)
                    cv.imshow(f"BlackJAI Server Feed - Mode: {self.view_mode}", image)
                    cv.waitKey(1)
            elif self.view_mode == "detect":
                while True:
                    # Receive image from publisher and convert to numpy array
                    msg, frame = receiver.receive(timeout=4)
                    image = np.array(cv.imdecode(np.frombuffer(frame, dtype='uint8'), -1))

                    # Detect image
                    # image, json_data = detect_card_type_roboflow(image, self.rf_model)

                    # Detect image using YOLO
                    image, json_data = detect_card_type_yolo(image, self.yolo_model)

                    # Display image
                    cv.imshow(f"BlackJAI Server Feed - Mode: {self.view_mode}", image)
                    cv.waitKey(1)
            elif self.view_mode == "process":
                while True:
                    # Receive image from publisher and convert to numpy array
                    msg, frame = receiver.receive(timeout=4)
                    image = np.array(cv.imdecode(np.frombuffer(frame, dtype='uint8'), -1))

                    # Detect image using Roboflow
                    # image, json_data = detect_card_type_roboflow(image, self.rf_model)

                    # Detect image using YOLO
                    image, json_data = detect_card_type_yolo(image, self.yolo_model)

                    # Update engine
                    engine.update(json_data)

                    # Send UDP message
                    # TODO: send udp message(s) to BlackJAI-Connect clients

                    # Display image
                    cv.imshow(f"BlackJAI Server Feed - Mode: {self.view_mode}", image)
                    cv.waitKey(1)
            elif self.view_mode == "picture":
                # Receive image from publisher and convert to numpy array
                msg, frame = receiver.receive(timeout=4)
                image = cv.imdecode(np.frombuffer(frame, dtype='uint8'), -1)
                print(image)
                # Get datetime
                now = datetime.datetime.now()
                # save image to disk with name as datetime
                print("saving")
                cv.imshow(f"BlackJAI Server Feed - Mode: {self.view_mode}", image)
                cv.waitKey(0)
                success = cv.imwrite(f"{os.getcwd()}/blackjai_server/data/pictures/{now.strftime('%Y_%m_%d__%H_%M_%S')}.jpg", image)
                print(success)
            elif self.view_mode == "timed_video":
                # Receive image from publisher and convert to numpy array
                msg, frame = receiver.receive(timeout=4)
                image = cv.imdecode(np.frombuffer(frame, dtype='uint8'), -1)
                # Get size of image
                height, width, layers = image.shape
                # Set timer using datetime
                start_time = datetime.datetime.now()
                # Create video writer
                result = cv.VideoWriter(f"./BlackJAI/dev/blackjai-server/blackjai_server/data/videos/{start_time.strftime('%Y_%m_%d__%H_%M_%S')}.avi",
                                        cv.VideoWriter_fourcc(*'MJPG'), 10, (width, height))
                while True:
                    # Receive image from publisher and convert to numpy array
                    msg, frame = receiver.receive(timeout=4)
                    image = cv.imdecode(np.frombuffer(frame, dtype='uint8'), -1)
                    # Write image to video
                    result.write(image)
                    # Display image
                    # if it has been 10 seconds, break
                    if (datetime.datetime.now() - start_time).seconds >= 20:
                        break
                    cv.imshow(f"BlackJAI Server Feed - Mode: {self.view_mode}", image)
                    cv.waitKey(100)
                # Release video
                result.release()

        except (KeyboardInterrupt, SystemExit):
            print('Exit due to keyboard interrupt')
        except Exception as ex:
            print('Python error with no Exception handler:')
            print('Traceback error:', ex)
            traceback.print_exc()
        finally:
            receiver.close()
            sys.exit()


"""
VideoStreamSubscriber:
This class is used to receive images from the publisher.
It acts as an asynchronous wrapper around the ImageHub class,
allowing us to receive images in a non-blocking manner.
"""
class VideoStreamSubscriber:

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self._stop = False
        self._data_ready = threading.Event()
        self._thread = threading.Thread(target=self._run, args=())
        self._thread.daemon = True
        self._thread.start()

    def receive(self, timeout=15.0):
        flag = self._data_ready.wait(timeout=timeout)
        if not flag:
            raise TimeoutError("Error: Timeout while reading from subscriber tcp://{}:{}".format(self.hostname, self.port))
        self._data_ready.clear()
        return self._data

    def _run(self):
        receiver = imagezmq.ImageHub("tcp://{}:{}".format(self.hostname, self.port), REQ_REP=False)
        while not self._stop:
            self._data = receiver.recv_jpg()
            self._data_ready.set()
        receiver.close()

    def close(self):
        self._stop = True


# Simulating heavy processing load
def limit_to_2_fps():
    sleep(0.5)
