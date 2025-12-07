from board import Position

class Board():
    def __init__(self, time:int = 6, condition:str = None, timeConditions:dict = dict()):
        """
        Creates an instance of Board

        :param time: integer representing the number of locations for card placement (6 if blank)
        :param condition: string representing the condition of the board
        :param timeConditions: dict containing times mapped to their condition
        """
        self.time = time
        self.condition = condition
        self.timeConditions = timeConditions
        self.create()


    def create(self):
        """
        Creates the board, with each Position and their condition
        """
        self.times = dict()
        for i in range(1, self.time+1):
            self.times[i] = Position(condition=self.timeConditions.get(i, ""))

    def addCardtoPos(self):
        pass

    def removeCardfromPos(self):
        pass

    def clear(self):
        pass

    