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

        # A new FSM is created
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


    @classmethod
    def thompsonConcat(self, aut1, aut2):

        # A new FSM is created
        concatFSM = transitionTable()
        concatFSM.copyFromFSM(aut1)
        concatFSM.copyFromFSM(aut2)

        # A new Epsilon transition is created between the final aut1 state and the initial aut2 state
        aut1FinalId = aut1.getOnlyFinalId()
        concatFSM.addEpsilon(aut1FinalId, aut2.initial)

        # aut1 final state is not final anyomre
        concatFSM.setFinalState(aut1FinalId, False)

        # aut1 initial state is the only initial state
        concatFSM.setInitial(aut1.initial.stateId)

        return concatFSM


    @classmethod
    def thompsonKleene(self, aut1):

        # A new FSM is created
        kleeneFSM = transitionTable()
        kleeneFSM.copyFromFSM(aut1)

        # A new final state is appended to the old final state
        newFinalId = self.getUniqueId()
        newFinal = kleeneFSM.addState(newFinalId, True)
        oldFinalId = kleeneFSM.getOnlyFinalId()
        kleeneFSM.addEpsilon(oldFinalId, newFinal)
        kleeneFSM.setFinalState(oldFinalId, False)

        # A new initial state is added. It transitions via Epsilon to the old one
        newInitialId = self.getUniqueId()
        kleeneFSM.addState(newInitialId, False)
        
        oldInitial = kleeneFSM.initial
        kleeneFSM.addEpsilon(newInitialId, oldInitial)
        kleeneFSM.setInitial(newInitialId)

        # The new initial state can transition to the new final state via Epsilon
        kleeneFSM.addEpsilon(newInitialId, newFinal)

        # The old final state can transition to the old initial state via Epsilon
        kleeneFSM.addEpsilon(oldFinalId, oldInitial)

        return kleeneFSM


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

    # test concat
    print("\n\n- Concatenation Test -")
    concat = Thompson.thompsonConcat(basicA, basicB)
    concat.printTransitions()

    # test kleene
    print("\n\n- Kleene Test -")
    kleene = Thompson.thompsonKleene(basicA)
    kleene.printTransitions()



