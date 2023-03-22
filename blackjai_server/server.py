import sys
import traceback
import cv2 as cv
import imagezmq
import threading
import numpy as np
from time import sleep


"""
BlackJAIServer:
This class is used to start the server and receive images from the publisher.
"""
class BlackJAIServer:
    def __init__(self, hostname="127.0.0.1", port=5555, view_mode="view"):
        self.hostname = hostname
        self.port = port
        self.view_mode = view_mode

    def start(self):
        receiver = VideoStreamSubscriber(self.hostname, self.port)
        # //TODO: instantiate engine
        # engine = BlackJAIEngine()

        try:
            if self.view_mode == "view":
                while True:
                    # Receive image from publisher
                    msg, frame = receiver.receive(timeout=2)

                    # Display image
                    image = cv.imdecode(np.frombuffer(frame, dtype='uint8'), -1)
                    cv.imshow(f"BlackJAI Server Feed - Mode: {self.view_mode}", image)
                    cv.waitKey(1)
            elif self.view_mode == "process":
                while True:
                    # Receive image from publisher
                    msg, frame = receiver.receive(timeout=2)
                    image = cv.imdecode(np.frombuffer(frame, dtype='uint8'), -1)

                    # Preprocess image
                    # //TODO: Use function from preprocessing.py

                    # Detect image
                    # //TODO: Use function from detection.py

                    # Update engine
                    # //TODO: Use update funtion from engine.py

                    # Send UDP message
                    # //TODO: send udp message(s) to BlackJAI-Connect clients

                    # Display image
                    cv.imshow(f"BlackJAI Server Feed - Mode: {self.view_mode}", image)
                    cv.waitKey(1)

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
            raise TimeoutError(
                "Timeout while reading from subscriber tcp://{}:{}".format(self.hostname, self.port))
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
