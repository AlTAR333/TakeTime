from assets.board import Board
from assets.deck import Deck
from assets.location import Location
from assets.hand import Hand

class Game():
    def __init__(self):
        pass

    def dealHands(self) -> None:
        self.hands = {player : Hand() for player in self.playersNames}
        player_pointer = 0
        for _ in range(12):
            # Draw card and add it to player's hand
            card = self.deck.draw()
            playerName = self.playersNames[player_pointer]
            self.hands[playerName].addCard(card)

            # Go to the next player
            player_pointer += 1
            if player_pointer == len(self.playersNames):
                player_pointer = 0

    def printHands(self) -> None:
        print("HANDS")
        for player, hand in self.hands.items():
            print(f"{player} : {hand}")

    def printBoard(self) -> None :
        print("BOARD")
        print(f"{self.board}")

    def preset1(self) -> None:
        """
        Basic game, 24 max per location
        """
        self.deck = Deck(shuffled = True)
        self.board = Board()
        

    def preset2(self):
        """

        """
        pass

    def preset3(self):
        """
        
        """
        pass

    def main(self) -> None:
        # Players
        self.players = int(input("Number of player : "))
        self.playerConfig = input("Do you want to name the players (Y/N) : ")
        if self.playerConfig == "Y":
            self.playersNames = []
            for i in range(1, self.players+1):
                playerName = input(f"Player {i} : ")
                self.playersNames.append(playerName)
        else :
            self.playersNames = [str(i) for i in range(1, self.players+1)]

        # Preset load
        self.preset = input("What preset do you want to load : ")
        if self.preset == "1":
            self.preset1()
        elif self.preset == "2":
            self.preset2()
        elif self.preset == "3":
            self.preset3()
        else :
            raise "Preset not found"
        
        # Start Game
        self.dealHands()
        print("=============================")
        self.printHands()
        print("")
        self.printBoard()


game = Game()
game.main()
