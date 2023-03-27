import csv
import pandas as pd

filename = "weather_data.csv"

with open(filename) as file:
    data = csv.reader(file)
    temperature = []
    for row in data:  # File has to be open for data.row to be called
        temperature += [row[1]]
        print(row)
    del temperature[0]

print(data)
print(temperature)

[print('-'*30+'\n') for _ in range(3)]

data = pd.read_csv(filename)
print(data)
print(type(data))

temp_list = data["temp"].to_list()

print(sum(temp_list)/len(temp_list))
print(data["temp"].mean())
print(data.temp.mean())

new_df_dic = {
    "students": ["Amy", "James", "Angela"],
    "score": [76, 56, 65]
}
df = pd.DataFrame(new_df_dic)
print(df)
df.to_csv("new_file.csv", index=False)
