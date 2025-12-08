from assets.location import Location

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
        Creates the board, with each Location and their condition
        """
        self.times = dict()
        for i in range(1, self.time+1):
            self.times[i] = Location(condition=self.timeConditions.get(i, ""))

    def addCardtoPos(self, location:int, card:tuple):
        """
        Add a card to a location

        :param location: integer representing the location
        :param card: tuple representing the added card
        """
        self.times[location].addCard(card)

    def removeCardfromPos(self, location:int, instruction:str = "top"):
        """
        Add a card to a location

        :param location: integer representing the location
        :param instruction: string used to determine the method of removal (top if blank),
                            "random" -> pop randomly
                            "highest" -> pop highest card in hand
                            "lowest" -> pop lowest card in hand
                            "top" -> pop top card, most left card
                            "bottom" -> pop bottom card, most right card
        """
        self.times[location].removeCard(instruction)

    def clear(self):
        """
        Clear all the locations
        """
        for location in self.times.values():
            location.clear()

    def __str__(self):
        board = ""
        for time in range(1, self.time+1):
            board += f"{time}: {self.times[time]} (count={self.times[time].size}, sum={self.times[time].getSum()})\n"
            # f"{time}: {self.times[time]} \n"
        return board
    
    def checkConditions(self) -> bool:
        """
        Check if all the conditions are respected
        """
        #TODO Add all the conditions and tests
        locationSums = []
        maxSumLocations = {i : 24 for i in range(1, self.time+1)} # Limit each location to a sum of 24
        minCardLocation = {i : 1 for i in range(1, self.time+1)} # Minimum number of cards per location
        for time, location in self.times.items(): # Test the global condition for every location
            locationSum = location.getSum()
            locationSums.append(locationSum)
            if locationSum > maxSumLocations[time]:
                return False
            locationSize = location.size
            if locationSize < minCardLocation[time]:
                return False
            if not location.checkCondition():
                return False

        return locationSums == sorted(locationSums)