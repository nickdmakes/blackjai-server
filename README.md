<!-- PROJECT LOGO -->
<div align="center">
<h1 align="center">blackjai-server</h1>

  <p align="center">
    Responsible for image data preprocessing and the game state engine behind BlackJAI system
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

BlackJAI Server is a python application that inputs a video stream of Black Jack game, preprocesses frames, detects cards, and tracks game state in order to determine most optimal action in the game of BlackJack.

> [!IMPORTANT]  
> This project only processes images that are recieved over the network from imagezmq. You will need to configure your own image broadcast application to send images to the blackjai-server. This repository is shown to showcase project work for recruiter interest

See more details on my [LinkedIn Projects Page](https://www.linkedin.com/in/nicholas-matthews713/details/projects/)

### Built With

* Python
* imagezmq
* OpenCV
* roboflow


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

### Installation

1. Clone the repo and navigate into the directory
   ```sh
   git clone https://github.com/nickmatthews713/blackjai-server.git
   cd blackjai-server
   ```
3. Create a python virtual enviornment and activate
   ```sh
   python3 -m virtualenv venv
   source venv/bin/activate
   ```
4. Install the required python packages
   ```sh
   pip install requirements.txt
   ```

<!-- USAGE EXAMPLES -->
## Usage

### Configure the Server

Edit the configuration file **conf.py** to change server settings

### Run the Server

To start the server...
```sh
python main.py
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- CONTACT -->
## Contact

Nick Matthews - nickd.mf7@gmail.com  

Project Link: [https://github.com/nickmatthews713/blackjai-server](https://github.com/nickmatthews713/blackjai-server)

<p align="right">(<a href="#top">back to top</a>)</p>
