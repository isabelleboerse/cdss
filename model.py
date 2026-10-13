import random
import numpy as np
import pandas as pd
import gdown
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier


df = pd.read_csv(r"C:\Users\isabe\cdss\borstkanker.csv", sep=';')

print(df.head())
print(df.shape)



