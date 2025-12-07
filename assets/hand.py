import random
from collections import deque

class Hand():
    def __init__(self):
        """
        Creates an instance of Hand
        """
        self.hand = deque()
        self.size = 0 # Size of the hand

    def setCards(self, cards:list):
        """
        Clear the hand and add the new ones

        :param cards: list of the cards
        """
        self.hand = deque(cards)
        self.size = len(self.cards)

    def addCard(self, card:tuple) -> None:
        """
        Add a given card to the top of the hand
    
        :param card: tuple representing a card
        """
        self.hand.append(card)
        self.size += 1

    def removeCard(self, instruction:str = "random") -> tuple:
        """
        Remove a card from the hand, depending on instruction

        :param instruction: string used to determine the method of removal (random if blank),
                            "random" -> pop randomly
                            "highest" -> pop highest card in hand
                            "lowest" -> pop lowest card in hand
                            "top" -> pop top card, most left card
                            "bottom" -> pop bottom card, most right card
        """
        assert len(self.hand) > 0, "Attempt to remove card from an empty hand"

        if instruction == "random":
            card = self.hand.remove(random.choice(self.hand))
        elif instruction == "highest":
            card = max(self.hand, key=lambda x: x[1])
            self.hand.remove(card)
        elif instruction == "lowest":
            card = min(self.hand, key=lambda x: x[1])
            self.hand.remove(card)
        elif instruction == "top":
            card = self.hand.pop()
        elif instruction == "bottom":
            card = self.hand.popleft()
        else :
            raise "Invalid instruction argument for removeCard() method."
        
        self.size -= 1
        return card

    def sort(self, order = "asc") -> None:
        """
        Sort the hand in ascending, descending, or random order

        :param order: string that determines the order in wich the hand is sorted (asc, desc, or rand, asc if blank) 
        """
        if order == "asc":
            self.hand.sort(key=lambda x: x[1])
        elif order == "desc":
            self.hand.sort(key=lambda x: x[1], reverse=True)
        elif order == "rand":
            random.shuffle(self.hand)
        else :
            raise "Invalid order argument for sort() method."

    def clear(self):
        """
        Clear the hand by removing all cards
        """
        self.hand = deque()

    def __str__(self):
        hand = ""
        for card in self.hand:
            color = card[0]
            number = card[1]
            hand += f"{number}{color[0].upper()} "
        return hand
    
    def getMax(self) -> int:
        """
        Returns the value of the highest card in hand
        """
        return max(self.hand, key=lambda x: x[1])[1]
