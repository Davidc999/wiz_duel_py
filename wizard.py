from spell_tree import Tree, two_handed_spell
from player_base import PlayerBase
import glossary
from wizard_turn import WizardTurn, SpellCast
from entity import Entity


class Wizard(Entity):
    # TODO: Whenever we have a list of list for spells on each hand, have a dictionary with{'left': [], 'right':[]}
    # TODO: Same for the list of hands
    def __init__(self, controlling_player: PlayerBase):
        self.gestureHistory = [[], []]
        self.spellTrees = {hand: Tree() for hand in glossary.HAND_NAMES}
        self.cast_lightning_short = False
        self.controlling_player = controlling_player
        self.controlling_player.print("Welcome to Wizard Duel!\n")
        name = self.controlling_player.get_input('What\'s you\'re name?')
        super(Wizard, self).__init__(15, name)

    def play_turn(self, entities: list) -> WizardTurn:
        """
        This function asks the player to enter their gestures, then it creates a WizardTurn object.
        It resolves the gestures and asks the player for targets for any resulting spells.
        :param entities: a list of entities that exist in the game. These are used to select targets.
        :return: WizardTurn object with the spells cast by the wizard and their targets.
        """
        gest = self.controlling_player.get_gestures('Please enter you next move <L, R>:', 2)
        wizard_turn = self.execute_gestures(gest)
        self.select_targets(wizard_turn, entities)
        return wizard_turn

    def execute_gestures(self, gestures: list) -> WizardTurn:
        """
        This function gets the player-entered gestures. It stores the gestures in the player history,
        resolves spell conflicts and creates a WizardTurn object with cast spells and surrender bool.
        :param gestures: a list of gestures entered by the player.
        :return: WizardTurn object with the spells cast by the user, but no targets for them.
        """
        gestures = self._validate_gestures(gestures)

        # Record gestures in Wizard's personal history.
        for gestnum in range(len(self.gestureHistory)):
            self.gestureHistory[gestnum].append(gestures[gestnum])
            # TODO: Remember that we only care about the last 8 gestures for any spell.
            # So keep record, but no need to display more than that later on.
            #self.gestureHistory[gestnum] = self.gestureHistory[gestnum][-8:]

        # Walk the spell state machine
        spells_cast = self.update_tree(gestures)

        # Handle surrender
        surrender = False
        if glossary.SURRENDER in spells_cast[glossary.HAND_NAMES[0]]:
            surrender = True
            for _, spell_set in spells_cast.items():
                spell_set.remove(glossary.SURRENDER)

        # Handle conflicts:
        final_spells_cast = {}
        for hand, spell_set in spells_cast.items():
            if len(spell_set) > 1:
                selected_spell = self.controlling_player.get_list_item(
                    '{} hand has completed multiple spells. Choose one:'.format(hand.capitalize()),
                    [spell + ' (two handed)' if spell in two_handed_spell else spell for spell in spell_set]
                )
                final_spells_cast[hand] = selected_spell
                if selected_spell in two_handed_spell:  # Both hands are casting same spell, so return
                    final_spells_cast = {hand: selected_spell for hand in glossary.HAND_NAMES}
                    break
            elif spell_set:
                final_spells_cast[hand] = spell_set.pop()
        return WizardTurn(final_spells_cast, surrender, self)
        #return final_spells_cast, surrender

    def update_tree(self, gestures: list):
        spells_cast = {hand: set() for hand in glossary.HAND_NAMES}
        for hand, gest in zip(glossary.HAND_NAMES, gestures):
            spells_cast[hand].update(self.spellTrees[hand].walkTree(gest))

        # Handle two-handed spells. Add them to both hands:
        spells_cast_copy = spells_cast.copy()
        for hand, spell_set in spells_cast.items():
            for spell in spell_set:
                if spell in two_handed_spell:
                    for _, hand_set in spells_cast_copy.items():
                        hand_set.add(spell)

        return spells_cast_copy

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
        for spell_cast_obj in wiz_turn.spell_cast_list:
            spell_cast_obj.set_target(
                self.controlling_player.get_list_item(
                    "Select a target for {}:".format(spell_cast_obj.spell),
                    entities
                )
            )





