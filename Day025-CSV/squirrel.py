import pandas as pd
filename = "squirrel_count.csv"

df = pd.read_csv(filename)
print(df['Primary Fur Color'].value_counts())
