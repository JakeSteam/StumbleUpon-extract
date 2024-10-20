import pandas as pd
import csv

df = pd.read_csv('data-parsed/parsed.csv')
# df = df[df['source'] != 'toprated'] # Remove top rated
# df = df[df['source'] == 'toprated'] # Keep only top rated
df = df.drop_duplicates(subset='id', keep='last')
df.to_csv('data-parsed/parsed-cleaned.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)