import random
from collections import deque

class Position():
    def __init__(self, cards:list = [], condition:str = ""):
        """
        Creates an instance of Position

        :param cards: list of cards already placed on that position
        :param condition: 
        """
        self.condition = condition
        self.iniCards = cards
        self.cards = deque(self.iniCards)
        self.size = len(cards)

    def setCards(self, cards):
        """
        Clear the position and add the new ones

        :param cards: list of the cards
        """
        self.cards = deque(cards)
        self.size = len(self.cards)

    def addCard(self, card):
        """
        Add a card to the position
        
        :param card: tuple represening the added card
        """
        self.cards.append(card)
        self.size += 1

    def removeCard(self, instruction:str = "random") -> tuple:
        """
        Remove a card from the position, depending on instruction

        :param instruction: string used to determine the method of removal (random if blank),
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
        Clear the position by removing all cards

        :param reset: If true, set the cards to the initial cards
        """
        if reset:
            self.cards = deque(self.iniCards)
            self.size = len(self.iniCards)
        else :
            self.cards = deque()
            self.size = 0