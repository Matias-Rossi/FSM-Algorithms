from copy import deepcopy

class state:
    def __init__(self, stateId, isFinal):
        self.stateId = stateId
        self.transitions = {}
        self.transitionsViaEpsilon = []
        self.isFinal = isFinal
        self.isInitial = False

    def addTransition(self, via, to):
        self.transitions[via] = to

    def addEpsilonTransition(self, to):
        self.transitionsViaEpsilon.append(to) 
            

    def getTransition(self, via):
        return self.transitions[via]

    def setFinal(self, newFinalValue):
        self.isFinal = newFinalValue
        
        
class transitionTable:
    def __init__(self):
        self.table = {}

    def copyFromFSM(self, oldFSM):
        copy = deepcopy(oldFSM.table)
        self.table.update(copy)
        self.initial = oldFSM.initial

    def addState(self, stateName, isFinal):
        self.table[stateName] = state(stateName, isFinal)
        return self.table[stateName]

    def addEntry(self, origin, via, to):
        self.table[origin].addTransition(via, to)

    def addEpsilon(self, origin, to):
        self.table[origin].addEpsilonTransition(to)

    def setInitial(self, stateId):
        # Assert that there is only one initial state
        for (_stateId, _stateData) in self.table.items():
            _stateData.isInitial = False
        # Set new initial state
        self.initial = self.table[stateId]
        self.table[stateId].isInitial = True

    def unassignInitial(self):
        self.initial.isInitial = False
        self.initial = None

    def transition(self, char):
        self.currentState = self.table[self.currentState].getTransition(char)

    def setFinalState(self, stateName, isFinal):
        self.table[stateName].setFinal(isFinal)

    def isInFinalState(self):
        return self.table[self.currentState].isFinal

    def printTransitions(self):
        print("- Printing Finite State Machine -")

        for (stateName, stateData) in self.table.items():

            if self.table[stateName].isInitial:
                print(f"\t'{stateName}' is initial")
            if self.table[stateName].isFinal:
                print(f"\t'{stateName}' is final")

            for (via, to) in stateData.transitions.items():
                print(f"\t'{stateName}' via '{via}' directs to '{self.table[stateName].transitions[via]}'")
            for (dest) in stateData.transitionsViaEpsilon:
                print(f"\t'{stateName}' via 'Epsilon' directs to '{dest.stateId}'")

        print("- End of Print -")


    def getOnlyFinalId(self):
        for (stateName, stateData) in self.table.items():
            if stateData.isFinal:
                return stateName


    def startAutomata(self, stream):
        self.currentState = self.initial
        for char in stream:
            try:
                self.transition(char)
            except KeyError:
                return False
        return self.isInFinalState


            

if __name__ == '__main__':
    transitionTable = transitionTable()
    transitionTable.addState('q0', False)
    transitionTable.addState('q1', True)
    transitionTable.addEntry('q0', 'a', 'q1')
    transitionTable.addEntry('q1', 'a', 'q1')
    transitionTable.setInitial('q0')

    if transitionTable.startAutomata('aaaaaaaa'):
        print('Accepted')
    else:
        print('Rejected')