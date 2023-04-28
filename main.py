from blackjai_server.server import BlackJAIServer
import sys
from conf import *


def main():
    print("Starting BlackJAIServer...")
    # Get first command line argument
    if len(sys.argv) > 1:
        vm = sys.argv[1]
    else:
        vm = VIEW_MODE
    server = BlackJAIServer(hostname=BLACKJAI_CAPTURE_IP, port=BLACKJAI_CAPTURE_PORT, view_mode=vm)
    server.start()


if __name__ == "__main__":
    main()
