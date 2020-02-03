from spell_tree import Tree, two_handed_spell
from player_base import PlayerBase
import glossary
from wizard_turn import WizardTurn, SpellCast
from entity import Entity


class Wizard(Entity):
    def __init__(self, controlling_player: PlayerBase):
        self.gestureHistory = [[], []]
        self.spellTrees = [Tree(), Tree()]
        self.cast_lightning_short = False
        self.controlling_player = controlling_player
        self.controlling_player.print("Welcome to Wizard Duel!\n")
        name = self.controlling_player.get_input('What\'s you\'re name?')
        super(Wizard, self).__init__(15, name)

    def play_turn(self, entities: list):
        gest = self.get_gestures()
        while not self.validate_gesture_input(gest):
            self.controlling_player.print("There has been a problem processing your input. Please try again.")
            gest = self.get_gestures()
        wizard_turn = self.execute_gestures(gest)
        self.select_targets(wizard_turn)
        return wizard_turn

    def get_gestures(self):
        player_gest = self.controlling_player.get_input('Please enter you next move <L, R>:')
        gestures = player_gest.upper().replace(" ", "").split(',')
        return gestures

    def execute_gestures(self, gestures: list):
        gestures = self._validate_gestures(gestures)

        # Record gestures in Wizard's personal history.
        for gestnum in range(len(self.gestureHistory)):
            self.gestureHistory[gestnum].append(gestures[gestnum])
            # TODO: Remember that we only care about the last 8 gestures for any spell.
            # So keep record, but no need to display more than that later on.
            #self.gestureHistory[gestnum] = self.gestureHistory[gestnum][-8:]
        spells_cast = self.update_tree(gestures)

        # Handle surrender
        surrender = False
        if 'surrender' in spells_cast[0]:
            surrender = True
            for spell_list in spells_cast:
                spell_list.remove('surrender')

        # Handle conflicts:
        final_spells_cast = []
        for list_num, spell_list in enumerate(spells_cast):
            if len(spell_list) > 1:
                selected_spell = self.controlling_player.get_list_item(
                    '{} hand has completed multiple spells. Choose one:'.format(glossary.HAND_NAMES[list_num].capitalize()),
                    [spell + ' (two handed)' if spell in two_handed_spell else spell for spell in spell_list]
                )
                '''
                self.controlling_player.print('{} hand has completed multiple spells. Choose one:'.format(glossary.HAND_NAMES[list_num].capitalize()))
                for num, spell in enumerate(spell_list):
                    if spell in two_handed_spell:
                        spell += ' (two-handed)'
                    self.controlling_player.print('{}. {}'.format(num+1, spell))
                selection = int(self.controlling_player.get_input(""))
                selected_spell = spell_list[selection-1]'''
                final_spells_cast.append([selected_spell])
                if selected_spell in two_handed_spell:  # Both hands are casting same spell, so return
                    final_spells_cast.append([selected_spell])
                    return final_spells_cast
            else:
                final_spells_cast.append(spell_list)
        return WizardTurn(final_spells_cast, surrender, self)
        #return final_spells_cast, surrender

    def update_tree(self, gestures: list):
        spellscast = []
        for gestnum in range(len(gestures)):
            spellscast.append(self.spellTrees[gestnum].walkTree(gestures[gestnum]))

        # Handle two-handed spells. Add them to both hands:
        for num, spell_list in enumerate(spellscast):
            for spell in spell_list:
                if spell in two_handed_spell and spell not in spellscast[len(spellscast)-1 - num]:
                    spellscast[len(spellscast)-1 - num].append(spell)

        return spellscast

    def _validate_gestures(self, gestures):
        if gestures[0] != gestures[1] and gestures[0] == 'C':
            print('Clapping with one hand amounts to nothing')
            gestures[0] = '.'
        elif gestures[0] != gestures[1] and gestures[1] == 'C':
            print('Clapping with one hand amounts to nothing')
            gestures[1] = '.'
        elif gestures[0] == gestures[1] and gestures[0] == '>':
            print('A wizard only has 1 dagger! Your right hand does nothing')
            gestures[1] = '.'
        elif gestures[0] == gestures[1]:
            gestures[0] = gestures[0].lower()
            gestures[1] = gestures[1].lower()
        return gestures

    def select_targets(self, wiz_turn: WizardTurn, entities: list):
        for spell in wiz_turn.spell_cast_list:
            spell.set_target(
                self.controlling_player.get_list_item(
                    "Select a target for {}:".format(spell[0]),
                    entities
                )
            )
            '''self.controlling_player.print("Select a target for {}:".format(spell[0]))
            for num, spell in enumerate(entities):
                self.controlling_player.print('{}. {}'.format(num+1, spell))
            selection = int(self.controlling_player.get_input(""))
            target_list.append([list[selection-1]])
            # Handle two-handed:
            if spell in two_handed_spell:
                target_list.append([list[selection-1]])
                return target_list'''




