from spell_library import SPELL_LIBRARY, Spell


#spelldict = {seq: name for name, seq in zip(spellNames, spellList)}


class Node:
    def __init__(self, name):
        self.children = {}
        self.spell_cast = None
        self.node_name = name


class Tree:
    def __init__(self):
        self.root = Node('')
        self.state = [self.root]
        self.prev_state = [self.root]
        spelldict = {spell_obj.gestures: spell_obj for spell_obj in SPELL_LIBRARY.values()}
        for k in spelldict:
            self.addSpell(spelldict[k], k)

    def addSpell(self, spell_obj: Spell, seq: str):
        func_node = self.root
        for gest in seq:
            if gest not in func_node.children:
                func_node.children[gest] = Node(func_node.node_name + gest)
            func_node = func_node.children[gest]
        func_node.spell_cast = spell_obj

    def walkTree(self, gesture):
        # TODO: (Maybe not here) handle double handed spells occupying both hands.
        # TODO: Handle surrender. It's not a spell, from the rules it looks like it might be 'cast' with other spells!
        #  So the wizard may actually win before he surrenders!
        spells_completed = []
        new_state = [self.root]
        self.prev_state = self.state
        # Advance current spells
        for curr_node in self.state:
            # Handle double-handed gestures
            if gesture.islower():
                if gesture.upper() in curr_node.children:
                    new_state.append(curr_node.children[gesture.upper()])
            if gesture in curr_node.children:
                new_state.append(curr_node.children[gesture])
        # Check if a spell has been cast
        for curr_node in new_state:
            if curr_node.spell_cast:
                spells_completed.append(curr_node.spell_cast)
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

