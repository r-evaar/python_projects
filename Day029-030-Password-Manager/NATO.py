import pandas as pd
df = pd.read_csv('nato_phonetic_alphabet.csv')
dic = {row.letter: row.code for _, row in df.iterrows()}
while True:
    try:
        print([dic[c.upper()] for c in input('Enter a word: ')])
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
    else:
        break
