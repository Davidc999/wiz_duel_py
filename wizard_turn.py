from spell_tree import two_handed_spell
import glossary
from entity import Entity


class SpellCast:
    def __init__(self, spell, hand, caster):
        self.spell = spell
        self.caster = caster
        self.hand = hand
        self.target = None

    def set_target(self, target):
        self.target = target

    def __str__(self):
        return '<spell: {}, hand: {}, caster: {}, target: {}>'.format(self.spell, self.hand, self.caster, self.target)


class WizardTurn:
    def __init__(self, spell_list: list, surrender: bool, caster):
        self.surrender = surrender
        self.spell_cast_list = []
        self.spell_cast_list = self.construct_spell_cast_list(spell_list, caster)

    def construct_spell_cast_list(self, spell_list, caster):
        spell_cast_list = []
        if spell_list[0] and spell_list[0][0] in two_handed_spell:
            spell_cast_list.append(SpellCast(spell_list[0], 'both', caster)) # Rather than both use 'left and right'. This could allow us to potentially add hands XD
        else:
            for num, spell in enumerate(spell_list):
                if spell:
                    spell_cast_list.append(SpellCast(spell, glossary.HAND_NAMES[num], caster))

        return spell_cast_list

    def __str__(self):
        string = "<surrender: {}".format(self.surrender)
        for spell in self.spell_cast_list:
            string = string+ "\n" + str(spell)
        string = string + ">"
        return string
# TODO: Make this instead a list of spellUnits + surrender boolean
# Spellunit = {Spell, hand, caster, target) Maye it'd be cool for it to be able to describe itself?