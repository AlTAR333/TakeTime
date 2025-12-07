import random

class Deck():

    def __init__(self, colors:set = {"black","white"}, numbers:set = {i for i in range(1, 13)}):
        """
        Creates an instance of Deck, and calls self.create()
        
        :param colors: Set of the different possible colors (black and white if blank)
        :param numbers: Set of the different possible numbers (1-12 if blank)
        """
        self.colors = colors
        self.numbers = numbers
        self.create()
        

    def create(self):
        """
        Generate an unshuffled deck with the given colors and numbers
        """
        self.deck = []
        for color in self.colors:
            for number in self.numbers:
                self.deck.append((color, number))

    def shuffle(self):
        """
        Shuffle the deck
        """
        random.shuffle(self.deck)

    def draw(self) -> tuple :
        """
        Draws 1 card from the deck and return it
        """
        return self.deck.pop()