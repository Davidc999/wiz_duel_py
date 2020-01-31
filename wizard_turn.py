from spell_tree import two_handed_spell
import glossary
from entity import Entity


class WizardTurn():
    def __init__(self, spell_list: list, surrender: boolean, caster: Entity, target: Entity):
        self.surrender = surrender
        if spell_list[0] and spell_list[0] in two_handed_spell:
            self.spells_cast = {'both': spell_list[0]}
        else:
            self.spells_cast = {glossary.HAND_NAMES[num]: spell[0] for num, spell in enumerate(spell_list) if spell}
        self.caster = caster
        self.target = target
asdll;kads
asd
# TODO: Make this instead a list of spellUnits + surrender boolean
# Spellunit = {Spell, hand, caster, target) Maye it'd be cool for it to be able to describe itself?