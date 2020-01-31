from spell_tree import Tree, two_handed_spell
from player_base import PlayerBase
import glossary
from wizard_turn import WizardTurn


class Wizard(Entity):
    def __init__(self, controlling_player: PlayerBase):
        self.gestureHistory = [[], []]
        self.spellTrees = [Tree(), Tree()]
        self.cast_lightning_short = False
        self.controlling_player = controlling_player
        self.controlling_player.print("Welcome to Wizard Duel!\n")
        name = self.controlling_player.get_input('What\'s you\'re name?')
        super(Wizard, self).__init__(15, name)

    # TODO: Maybe this doesn't belong in this class?
    def validate_gesture_input(self, gest, length: int = 2) -> bool:
        if len(gest) != length:
            return False
        if any([x.lower() not in glossary.GESTURES for x in gest]):
            return False
        return True

    def play_turn(self, entities: list):
        gest = self.get_gestures()
        while not self.validate_gesture_input(gest):
            self.controlling_player.print("There has been a problem processing your input. Please try again.")
            gest = self.get_gestures()
        spells_cast, surrender = self.execute_gestures(gest)
        select_targets(spells_cast)
        return WizardTurn(spells_cast, surrender, self)

    def get_gestures(self):
        player_gest = self.controlling_player.get_input('Please enter you next move <L, R>:')
        gestures = player_gest.upper().replace(" ", "").split(',')
        return gestures

    def execute_gestures(self, gestures: list):
        gestures = self._validate_gestures(gestures)

        for gestnum in range(len(self.gestureHistory)):
            self.gestureHistory[gestnum].append(gestures[gestnum])
            self.gestureHistory[gestnum] = self.gestureHistory[gestnum][-8:]
        spells_cast = self.update_tree(gestures)

        # Handle surrender
        if 'surrender' in spells_cast[0]:
            surrender = True
            for list in spells_cast:
                list.remove('surrender')

        # Handle conflicts:
        final_spells_cast = []
        for list_num, list in enumerate(spells_cast):
            if(len(list) > 1):
                self.controlling_player.print('{} hand has completed multiple spells. Choose one:'.format(glossary.HAND_NAMES[list_num].capitalize()))
                for num, spell in enumerate(list):
                    if spell in two_handed_spell:
                        spell += ' (two-handed)'
                    self.controlling_player.print('{}. {}'.format(num+1, spell))
                selection = int(self.controlling_player.get_input(""))
                selected_spell = list[selection-1]
                final_spells_cast.append([selected_spell])
                if selected_spell in two_handed_spell: # Both hands are casting same spell, so return
                    final_spells_cast.append([selected_spell])
                    return final_spells_cast
            else:
                final_spells_cast.append(list)

        return final_spells_cast, surrender

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

    def select_targers(self, spells_cast: list, entities: list):
        target_list = []
        for spell in spells_cast:
            if spell:
                self.controlling_player.print("Select a target for {}:".format(spell[0]))
                for num, spell in enumerate(entities):
                    self.controlling_player.print('{}. {}'.format(num+1, spell))
                selection = int(self.controlling_player.get_input(""))
                target_list.append([list[selection-1]])
                # Handle two-handed:
                if spell in two_handed_spell:
                    target_list.append([list[selection-1]])
                    return target_list
            else:
                target_list.append([])
        return target_list




