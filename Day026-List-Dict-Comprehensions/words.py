import pandas as pd

sentence = "What is the Airspeed Velocity of an Unladen Swallow?"

print({word: len(word) for word in sentence.split(' ')})

weather_c = {
    "Monday": 12,
    "Tuesday": 14,
    "Wednesday": 15,
    "Thursday": 14,
    "Friday": 21,
    "Saturday": 22,
    "Sunday": 24
}

fahrenheit = lambda c: c*9/5 + 32
print({day: fahrenheit(temp) for day, temp in weather_c.items()})
