# Flight Bot
AI chat bot using Rasa NLU.

## Getting Started

### Prerequisites
The program is written in Python 3.7. Prerequisites are listed below. 
* rasa                      1.1.7
* rasa-nlu                  0.15.1
* rasa-sdk                  1.1.0
* amadeus                   3.1.0
* duckling                  latest version from docker
* python-telegram-bot       11.1.0

You can install rasa and amadeus with pip
```
pip install rasa
pip install rasa-nlu
pip install amadeus
pip install python-telegram-bot
```

The `duckling` can be ran from docker
```
docker run -p 8000:8000 rasa/duckling
```
Or you can [install duckling directly on your machine](https://github.com/facebook/duckling#quickstart) and start the server

### Training model
Before using the flight bot, you need to train the model first. The training is done by `train.py` and it will save the trained model to `./model`

### Demo
Search for @Larry88Bot on Telegram to see a demo.

## Usage
Clone the repository and make sure you've installed all dependencies. Start a `duckling` 
server.
```
docker run -p 8000:8000 rasa/duckling
```
Run the model training
```
python train.py
```
Trained model is saved to `./model`
Change the telegram bot API and Amadeus API key. Start running `telechat.py`
```
python telechat.py
```

## Built With
* [Rasa](https://rasa.com) - The natural language understanding framework used
* [Python Telegram Bot 11.1.0](https://python-telegram-bot.org/) - The wrapper used to access Telegram bot Api

## Author
* **Larry Li**
