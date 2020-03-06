"""
Author: Trevor Stalnaker
File: fsm.py

A class that models a finite state machine
"""

class FSM():
    """
    Models a generalized finite state machine
    """

    def __init__(self, startState, states, transitions):
        self._state = startState
        self._startState = startState
        self._states = states
        self._transitions = transitions

    def changeState(self, action):
        for rule in self._transitions:
            if rule.getStartState() == self._state and \
               rule.getAction() == action:
                self._state = rule.getEndState()
            
    def getCurrentState(self):
        return self._state

    def getStates(self):
        return self._states

    def getTransitions(self):
        return self._transitions

    def backToStart(self):
        self._state = self._startState

class Rule():
    """
    Models a transition in a finite state machine
    """

    def __init__(self, state1, action, state2):
        self._startState = state1
        self._action = action
        self._endState = state2

    def getStartState(self):
        return self._startState

    def getAction(self):
        return self._action

    def getEndState(self):
        return self._endState

    def __repr__(self):
        return "(" + str(self._startState) + "," + str(self._symbol) + \
               "," + str(self._endState) + ")"

