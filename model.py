from pathlib import Path
import pandas as pd

df = pd.read_csv(r"C:\Users\romay\cdss\borstkanker.csv", sep=';')

print(df.head())
print(df.shape)

