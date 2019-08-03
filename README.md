# Flight Bot
AI chat bot using Rasa NLU.

## Getting Started

### Prerequisites
The program is written in Python 3.7. You will need to install rasa nlu and amadeus(flight search API).
* rasa                      1.1.7
* rasa-nlu                  0.15.1
* rasa-sdk                  1.1.0
* amadeus                   3.1.0

You can install them with pip
```
pip install rasa
pip install rasa-nlu
pip install amadeus
```

### Training model
Before using the flight bot, you need to train the model first. The training is done by `train.py` and it will save the trained model to `./model`


## Built With
* [Rasa](https://rasa.com) - The natural language understanding framework used

## Author
* **Larry Li**
