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


class Spell:
    def __init__(self, **kwargs):
        self.name = kwargs['Spell name']
        self.gestures = kwargs['Gestures']
        self.implemented = kwargs['Implemented']
        self.type = kwargs['Type']
        self.is_two_handed = kwargs['Two-Handed']
        self.is_shieldable = kwargs['Shieldable']
        self.is_reflectable = kwargs['Reflectable']
        self.plan = kwargs['Plan']
        self.priority = kwargs['Priority']
        self.rules_string = kwargs['rules']

    def __str__(self):
        return self.name


SPELL_LIBRARY = {}
with open('Book2.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        new_row = {k: literal_eval(v) for k, v in row.items()}
        new_row['Type'] = SpellType[new_row['Type'].upper().replace(' ', '_')]
        #SPELL_LIBRARY[new_row['Spell name']] = new_row
        SPELL_LIBRARY[new_row['Spell name']] = Spell(**new_row)

SURRENDER = SPELL_LIBRARY['Surrender']