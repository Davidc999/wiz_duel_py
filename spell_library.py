import csv
from enum import Enum


class SpellType(Enum):
    GLOBAL_STATUS_EFFECT = 1
    HP_MODIFY = 2
    PERSONAL_STATUS_EFFECT = 3
    SPECIAL = 4
    SUMMON = 5


def literal_eval(string: str):
    if string.isnumeric():
        return int(string)
    if string.lower() == 'false':
        return False
    if string.lower() == 'true':
        return True
    return string


SPELL_LIBRARY = {}
with open('Book2.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        new_row = {k: literal_eval(v) for k, v in row.items()}
        new_row['Type'] = SpellType[new_row['Type'].upper().replace(' ', '_')]
        SPELL_LIBRARY[new_row['Spell name']] = new_row
