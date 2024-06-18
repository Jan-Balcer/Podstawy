import pandas as pd
import matplotlib.pyplot as plt

# Wczytywanie danych z pliku CSV
filename = 'RYNE.csv'
df = pd.read_csv(filename)

# Upewnijmy się, że dane są poprawnie wczytane
print(df.head())
