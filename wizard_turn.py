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
    def __init__(self, spell_list: dict, surrender: bool, caster):
        self.surrender = surrender
        self.spell_cast_list = []
        self.spell_cast_list = self.construct_spell_cast_list(spell_list, caster)

    def construct_spell_cast_list(self, spell_dict, caster):
        spell_cast_list = []
        for hand, spell in spell_dict.items():
            if spell.is_two_handed:  # Handle two-handed spells
                spell_cast_list.append(SpellCast(spell, '+'.join(glossary.HAND_NAMES), caster))
                break
            spell_cast_list.append(SpellCast(spell, hand, caster))

        return spell_cast_list

    def __str__(self):
        string = "<surrender: {}".format(self.surrender)
        for spell in self.spell_cast_list:
            string = string+ "\n" + str(spell)
        string = string + ">"
        return string

# Spellunit = {Spell, hand, caster, target) Maye it'd be cool for it to be able to describe itself?