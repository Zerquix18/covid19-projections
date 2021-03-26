import pandas

people = pandas.read_csv('data/personas.csv')

embarazadas_en_sus_21 = people.query('CONFIRMADO == 1 & FALLECIDO == 1')

print(embarazadas_en_sus_21)
