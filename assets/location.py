import random
from collections import deque

class Location():
    def __init__(self, cards:list = [], condition:str = ""):
        """
        Creates an instance of Location

        :param cards: list of cards already placed on that location
        :param condition: 
        """
        self.condition = condition
        self.iniCards = cards
        self.cards = deque(self.iniCards)
        self.size = len(cards)

    def setCards(self, cards):
        """
        Clear the location and add the new ones

        :param cards: list of the cards
        """
        self.cards = deque(cards)
        self.size = len(self.cards)

    def addCard(self, card):
        """
        Add a card to the location
        
        :param card: tuple representing the added card
        """
        self.cards.append(card)
        self.size += 1

    def removeCard(self, instruction:str = "top") -> tuple:
        """
        Remove a card from the location, depending on instruction

        :param instruction: string used to determine the method of removal (top if blank),
                            "random" -> pop randomly
                            "highest" -> pop highest card in hand
                            "lowest" -> pop lowest card in hand
                            "top" -> pop top card, most left card
                            "bottom" -> pop bottom card, most right card
        """
        assert len(self.hand) > 0, "Attempt to remove card from an empty hand"

        if instruction == "random":
            card = self.cards.remove(random.choice(self.hand))
        elif instruction == "highest":
            card = self.cards.remove(max(self.hand, key=lambda x: x[1]))
        elif instruction == "lowest":
            card = self.cards.remove(max(self.hand, key=lambda x: x[1]))
        elif instruction == "top":
            card = self.cards.pop()
        elif instruction == "bottom":
            card = self.cards.popleft()
        else :
            raise "Invalid instruction argument for removeCard() method."
        
        self.size -= 1
        return card

    def clear(self, reset:bool = False):
        """
        Clear the location by removing all cards

        :param reset: If true, set the cards to the initial cards
        """
        if reset:
            self.cards = deque(self.iniCards)
            self.size = len(self.iniCards)
        else :
            self.cards = deque()
            self.size = 0

    def __str__(self):
        location = ""
        for card in self.cards:
            color = card[0]
            number = card[1]
            location += f"{number}{color[0].upper()} "
        return location