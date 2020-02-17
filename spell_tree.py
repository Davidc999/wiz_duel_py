spellList = ["cDPW","cSWWS","cw","DFFDD","DFPW","DFW","DPP","DSF","DSFFFc","DWFFd","DWSSSP","DWWFWc","DWWFWD","FFF","FPSFW","FSSDD","P","p","PDWP","PPws","PSDD",
            "PSDF","PSFW","PWPFSSSD","PWPWWc","SD","SFW","SPF","SPFPSDW","SPPc","SSFP","SWD","SWWc","WDDc","WFP","WFPSFW","WPFD","WPP","WSSc","WWFP","WWP","WWS",">"]

spellNames = ["Dispel magic", "Summon elemental", "Magic mirror", "Lightning bolt", "Cure heavy wounds", "Cure light wounds", "Amnesia", "Confusion", "Disease",
            "Blindness", "Delayed effect", "Raise dead", "Poison", "Paralysis", "Summon troll", "Fireball", "Shield", "Surrender", "Remove enchantment", "Invisibility", "Charm monster",
            "Charm person", "Summon ogre", "Finger of death", "Haste", "Missile", "Summon goblin", "Anti-spell", "Permanency", "Time stop", "Resist cold", "Fear", "Fire storm",
            "Lightning bolt (short)", "Cause light wounds", "Summon giant", "Cause heavy wounds", "Counter-spell", "Ice storm", "Resist heat", "Protection from evil", "Counter-spell","stab"]

spelldict = {seq: name for name, seq in zip(spellNames, spellList)}
two_handed_spell = set([spelldict[x] for x in spelldict if x[-1].islower()])

class Node():
    def __init__(self, name):
        self.children = {}
        self.spell_cast = ''
        self.node_name = name


class Tree():
    def __init__(self):
        self.root = Node('')
        self.state = [self.root]
        self.prev_state = [self.root]
        for k in spelldict:
            self.addSpell(spelldict[k], k)

    def addSpell(self, spell_name, seq):
        func_node = self.root
        for gest in seq:
            if not gest in func_node.children:
                func_node.children[gest] = Node(func_node.node_name + gest)
            func_node = func_node.children[gest]
        func_node.spell_cast = spell_name

    def walkTree(self, gesture):
        # TODO: (Maybe not here) handle double handed spells occupying both hands.
        # TODO: Handle surrender. It's not a spell, from the rules it looks like it might be 'cast' with other spells!
        #  So the wizard may actually win before he surrenders!
        spells_completed = set()
        new_state = [self.root]
        self.prev_state = self.state
        # Advance current spells
        for curr_spell in self.state:
            # Handle double-handed gestures
            if gesture.islower():
                if gesture.upper() in curr_spell.children:
                    new_state.append(curr_spell.children[gesture.upper()])
            if gesture in curr_spell.children:
                new_state.append(curr_spell.children[gesture])
        # Check if a spell has been cast
        for curr_spell in new_state:
            if curr_spell.spell_cast:
                spells_completed.add(curr_spell.spell_cast)
        # Update state:
        self.state = new_state
        return spells_completed

    def step_back(self):
        self.state = self.prev_state
        self.prev_state = []

if __name__ == '__main__':
    t = Tree()

    while True:
        x = input('Enter next gesture:\n')
        if x == 'x':
            break
        elif x == '?':
            t.step_back()
        else:
            print(t.walkTree(x))

