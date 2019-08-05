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

You can install rasa and amadeus with pip
```
pip install rasa
pip install rasa-nlu
pip install amadeus
```

The `duckling` can be ran from docker
```
docker run -p 8000:8000 rasa/duckling
```
Or you can [install duckling directly on your machine](https://github.com/facebook/duckling#quickstart) and start the server

### Training model
Before using the flight bot, you need to train the model first. The training is done by `train.py` and it will save the trained model to `./model`


## Built With
* [Rasa](https://rasa.com) - The natural language understanding framework used

## Author
* **Larry Li**
