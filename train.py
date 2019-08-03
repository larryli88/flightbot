import time
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config

def trainModel():
    # loading training data
    training_data = load_data('atis_train.json')
    # create a trainer
    trainer = Trainer(config.load("config.yml"))
    # start training
    trainer.train(training_data)
    # save the trained model
    model_directory = trainer.persist('./model')

t = time.process_time()
#do some stuff
trainModel()
elapsed_time = time.process_time() - t
print(elapsed_time)