from automata import *

class Thompson:
    statesUsed = 0

    @classmethod
    def getUniqueId(self):
        self.statesUsed = self.statesUsed + 1
        return f'q{self.statesUsed - 1}'

    @classmethod
    def basicSymbol(self, symbol):
        symbolThompson = transitionTable()
        state1 = self.getUniqueId()
        state2 = self.getUniqueId()
        symbolThompson.addState(state1, False)
        symbolThompson.addState(state2, True)
        symbolThompson.addEntry(state1, symbol, state2)
        symbolThompson.setInitial(state1)
        return symbolThompson

    @classmethod
    def thompsonUnion(self, aut1, aut2):

        # New FSM is created
        unionFSM = transitionTable()
        unionFSM.copyFromFSM(aut1)
        unionFSM.copyFromFSM(aut2)

        # A new common initial state is created 
        newInitial = self.getUniqueId()
        unionFSM.addState(newInitial, False)

        # Epsilon transition direct to both old initial states
        for (key, _state) in unionFSM.table.items():
            if _state.isInitial == True:
                _state.isInitial = False
                unionFSM.addEpsilon(newInitial, _state)

        unionFSM.setInitial(newInitial)

        # A new common final state is created
        newFinal = self.getUniqueId()
        unionFSM.addState(newFinal, True)

        # Epsilon transition direct from both old final states to the new one
        for (key, _state) in unionFSM.table.items():
            if _state.isFinal == True and key is not newFinal:
                _state.isFinal = False
                unionFSM.addEpsilon(key, unionFSM.table[newFinal])

        return unionFSM

if __name__ == "__main__":
    # test Basic
    print("- Basic Test -")
    basic = Thompson.basicSymbol('a')
    basic.printTransitions()

    # test union
    print("\n\n- Union Test -")
    basicA = Thompson.basicSymbol('a')
    basicB = Thompson.basicSymbol('b')
    union = Thompson.thompsonUnion(basicA, basicB)
    union.printTransitions()



