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

    def addCardtoPos(self, position:int, card:tuple):
        """
        Add a card to a position

        :param position: integer representing the position
        :param card: tuple representing the added card
        """
        self.times[position].addCard(card)

    def removeCardfromPos(self, position:int, instruction:str = "top"):
        """
        Add a card to a position

        :param position: integer representing the position
        :param instruction: string used to determine the method of removal (top if blank),
                            "random" -> pop randomly
                            "highest" -> pop highest card in hand
                            "lowest" -> pop lowest card in hand
                            "top" -> pop top card, most left card
                            "bottom" -> pop bottom card, most right card
        """
        self.times[position].removeCard(instruction)

    def clear(self):
        """
        Clear all the positions
        """
        for position in self.times.values():
            position.clear()