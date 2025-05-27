import time
import random
import pandas as pd

# Load test data and model
test_data = pd.read_csv('test.csv')
model = ... # load your trained model

def get_random_input():
    row = test_data.sample(1).drop(columns=['id'])
    return row
