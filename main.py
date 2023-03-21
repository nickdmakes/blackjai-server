from blackjai_server.server import BlackJAIServer
from conf import *


def main():
    print("Starting BlackJAIServer...")
    server = BlackJAIServer(hostname=BLACKJAI_CAPTURE_IP, port=BLACKJAI_CAPTURE_PORT, view_mode=VIEW_MODE)
    server.start()
    

if __name__ == "__main__":
    main()
