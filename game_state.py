from wizard_turn import WizardTurn
class GameState():
    wizards = []
    entities = []
    global_status = []

    def play_turn(self, wiz_turns: list(WizardTurn)):
        all_spells = []
        for wiz_turn in wiz_turns:
            all_spells += wiz_turn.spell_cast_list



