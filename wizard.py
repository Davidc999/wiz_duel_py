from spell_tree import Tree, two_handed_spell
import glossary

class Wizard():
    def __init__(self, name='Player 1'):
        # inputmethod
        self.gestureHistory = [[], []]
        self.spellTrees = [Tree(), Tree()]
        self.cast_lightning_short = False
        self.name = name
        self.hp = 15

    def get_gestures(self):
        gestures = [x.strip(' ').upper() for x in input('Please enter you next move <L, R>:\n').split(',')]
        return gestures

    def execute_gestures(self, gestures):
        gestures = self._validate_gestures(gestures)

        for gestnum in range(len(self.gestureHistory)):
            self.gestureHistory[gestnum].append(gestures[gestnum])
            self.gestureHistory[gestnum] = self.gestureHistory[gestnum][-8:]
        spells_cast = self.update_tree(gestures)

        #TODO: This should eventually return a PlayerMove object, or some such thing.

        # Handle surrender
        if 'surrender' in spells_cast[0]:
            surrender = True
            for list in spells_cast:
                list.remove('surrender')

        #TODO: Complete handle conflict logic. It should pick the spell to cast for this hand and dump the rest.
        # Handle conflicts:
        final_spells_cast = []
        for list_num, list in enumerate(spells_cast):
            if(len(list) > 1):
                print('{} hand has completed multiple spells. Choose one:'.format(glossary.HAND_NAMES[list_num].capitalize()))
                for num, spell in enumerate(list):
                    if spell in two_handed_spell:
                        spell += ' (two-handed)'
                    print('{}. {}'.format(num+1, spell))
                selection = input()
                final_spells_cast.append([list[selection-1]])
            else:
                final_spells_cast.append(list)

        return final_spells_cast





    def update_tree(self, gestures):
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

